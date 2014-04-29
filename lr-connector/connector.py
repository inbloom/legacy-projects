import json
import urllib2
import urllib
import urlparse
import time
import logging
import pyes
from datetime import datetime
import lribhelper
import helperfunctions
from LRSignature.verify.Verify import Verify_0_21
import gnupg

class connector(object):


    def __init__(self):
        self.config = json.loads(helperfunctions.readFile('./config.json'))
        logging.basicConfig(filename='./connector.log', level=getattr(logging, self.config['logging_level']), format='%(asctime)s %(levelname)s %(message)s')
        self.lribhelper = lribhelper.lribhelper(self.config, logging)
        self.gpg = gnupg.GPG(gpgbinary = self.config['gpg']['binary'])
        self.verify = Verify_0_21(gpgbin = self.config['gpg']['binary'])


    def run(self):
        logging.info('Start')

        # Check if ElasticSearch index exists and create if needed
        index = self.config['lris']['index']
        logging.info('Checking for "{0}" index'.format(index))
        es = pyes.ES('{0}:{1}'.format(self.config['lris']['host'], self.config['lris']['port']))
        getIndicesResponse = es.get_indices()
        if index not in getIndicesResponse:
            logging.info('Index "{0}" not found, creating'.format(index))
            settings = json.loads(helperfunctions.readFile('./lrissettings.json'))
            createIndexResponse = es.create_index_if_missing(index, settings)
            if 'acknowledged' in createIndexResponse and createIndexResponse['acknowledged'] and \
                'ok' in createIndexResponse and createIndexResponse['ok']:
                logging.info('Successfully created index "{0}"'.format(index))
            else:
                raise Exception('Error creating index: {0}'.format(createIndexResponse))
            # The mapping uses dynamic templates so index the seed item to create the initial mapping for schema.org data
            seed = json.loads(helperfunctions.readFile('./seeditem.json'))
            es.index(seed, self.config['lris']['index'], self.config['lris']['index_type'], 'seed')
            es.delete(self.config['lris']['index'], self.config['lris']['index_type'], 'seed')
        logging.info('Index "{0}" exists, beginning harvest loop'.format(index))

        # Main harvest loop
        while True:
            fromDate = helperfunctions.readFile('./fromDate.txt')
            until = datetime.utcnow().isoformat() + "Z"
            logging.debug(str.format('Beginning Harvest from: {0} until: {1}', fromDate, until))
            self.doHarvest(fromDate, until)
            logging.debug(str.format('Completed Harvest from: {0} until: {1}', fromDate, until))
            helperfunctions.writeFile('./fromDate.txt', until)
            time.sleep(self.config['interval'])


    def doHarvest(self, fromDate, until):
        lrUrl = self.config['lr']['url']
        if not fromDate:
            fromDate = self.config['lr']['first_run_start_date']
        urlParts = urlparse.urlparse(lrUrl)
        params = {"until": until}
        if fromDate:
            params['from'] = fromDate
        newQuery = urllib.urlencode(params)
        lrUrl = urlparse.urlunparse((urlParts[0],
                                     urlParts[1],
                                     '/harvest/listrecords',
                                     urlParts[3],
                                     newQuery,
                                     urlParts[5]))
        resumption_token = self.harvestData(lrUrl)
        while resumption_token is not None:
            newQuery = urllib.urlencode({"resumption_token": resumption_token})
            lrUrl = urlparse.urlunparse((urlParts[0],
                                     urlParts[1],
                                     '/harvest/listrecords',
                                     urlParts[3],
                                     newQuery,
                                     urlParts[5]))
            resumption_token = self.harvestData(lrUrl)


    def harvestData(self, lrUrl):
        resumption_token = None
        try:
            logging.debug("harvesting: " + lrUrl)
            resp = urllib2.urlopen(lrUrl)
            data = json.load(resp)
            for i in data['listrecords']:
                envelope = i['record']['resource_data']
                self.process(envelope)
            if "resumption_token" in data and \
               data['resumption_token'] is not None and \
               data['resumption_token'] != "null":
                resumption_token = data['resumption_token']
        except:
            logging.exception(str.format('lrUrl: {0}', lrUrl))
        return resumption_token


    def process(self, envelope):
        try:
            logging.debug(str.format('Processing: {0}', envelope['doc_ID']))
            if "LRMI" in [x.upper() for x in envelope['payload_schema']]:
                logging.debug('Processing LRMI Envelope')
                if self.validateSchemaDotOrg(envelope):
                    # Wait until now to validate the signature since it is resource intensive
                    verified = self.verifySignature(envelope)
                    if verified != None:
                        self.insertIntoElasticSearch(envelope)
                        self.insertIntoLrib(envelope, verified)
        except:
            logging.exception('Exception in process')


    def validateSchemaDotOrg(self, envelope):
        # basic validation
        try:
            if isinstance(envelope['resource_data']['items'], list) and \
                len(envelope['resource_data']['items']) == 1 and \
                envelope['resource_data']['items'][0]['type'][0] == "http://schema.org/CreativeWork" and \
                len(envelope['resource_data']['items'][0]['properties']['url']) == 1 and \
                (type(envelope['resource_data']['items'][0]['properties']['url'][0]) == str or \
                type(envelope['resource_data']['items'][0]['properties']['url'][0]) == unicode):
                return True
        except:
            pass
        return False


    def verifySignature(self, envelope):
        # Import any keys referenced in the envelope
        if 'digital_signature' in envelope:
            try:
                for location in envelope['digital_signature']['key_location']:
                    try:
                        result = self.gpg.import_keys(urllib2.urlopen(location).read())
                        if result.count == 0:
                            raise Exception('No key found at "{0}"'.format(location))
                        for fingerprint in result.fingerprints:
                            logging.debug('Imported key at "{0}" with fingerprint "{1}" from doc_ID "{2}"'.format(location, fingerprint, envelope['doc_ID']))
                    except:
                        logging.exception('Error importing key at "{0}"'.format(location))
            except:
                logging.exception('Error importing keys from doc_ID: {0}'.format(envelope['doc_ID']))
        # Verify the signature
        return self.verify.get_and_verify(envelope)


    def insertIntoElasticSearch(self, envelope):
        try:
            logging.debug(str.format('insertIntoElasticSearch with {0}', envelope['doc_ID']))
            item = envelope['resource_data']['items'][0]
            es = pyes.ES('{0}:{1}'.format(self.config['lris']['host'], self.config['lris']['port']))
            es.index(item, self.config['lris']['index'], self.config['lris']['index_type'], urllib.quote_plus(helperfunctions.scrubUrl(item['properties']['url'][0])))
        except:
            logging.exception(str.format('doc_ID: {0}', envelope['doc_ID']))


    def insertIntoLrib(self, envelope, verified):
        try:
            logging.debug(str.format('insertIntoLRIB with {0}', envelope['doc_ID']))
            if verified.fingerprint == self.config['lr']['public_key_fingerprint'] and \
                envelope['identity']['submitter'] == self.config['lr']['tagger_submitter']:
                # This is an envelope from Tagger so use the inBloom userId in the curator field
                if not ('curator' in envelope['identity'] and len(envelope['identity']['curator']) > 0):
                    raise Exception('curator not found in Tagger envelope')
                creatorId = 'urn:inbloom:user:{0}'.format(envelope['identity']['curator'])
            else:
                # This is an envelope that is properly signed but not from Tagger
                if 'curator' in envelope['identity'] and len(envelope['identity']['curator']) > 0:
                    user = envelope['identity']['curator']
                else:
                    user = envelope['identity']['submitter']
                creatorId = 'urn:lr:{0}:{1}'.format(verified.fingerprint, user)
            self.lribhelper.createEntity(envelope['resource_data']['items'][0], creatorId)
        except:
            logging.exception(str.format('doc_ID: {0}', envelope['doc_ID']))


if __name__ == "__main__":
    c=connector()
    c.run()
