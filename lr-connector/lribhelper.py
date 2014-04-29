import json
import urllib2
import urllib
import urlparse
import re
import helperfunctions
import base64
import datetime
import hashlib

class lribhelper(object):


    def __init__(self, config, logging):
        self.config = config
        self.logging = logging
        self.entityCache = {}
        # List of properties that can potentially be used as the entity ID in order of strength
        self.potentialEntityIdProperties = ['url', 'name', 'targetUrl', 'targetName']
        # Alignment Object is a special case, list of properties to be used in the hash for the entity ID
        self.alignmentObjectProperties = ['alignmentType', 'educationalFramework', 'targetDescription', 'targetName', 'targetUrl']


    def createEntity(self, entity, submitter):
        # Todo: in schema.org entities can have more than one type
        try:
            up = urlparse.urlparse(entity['type'][0])
            if up[1].lower() != 'schema.org' and not up[1].lower().endswith('.schema.org'):
                raise ValueError(str.format('invalid entity type: {0}', entity['type'][0]))
            entityType = self.makeLowercaseUnderscore(up[2])
            entityId = self.makeEntityId(entityType, entity)
            # Search for the entity by ID
            entitySearchResponse = self.entitySearchById(entityId)
            entityGuid = None
            if isinstance(entitySearchResponse['response'], list) and \
                len(entitySearchResponse['response']) > 0 and \
                'props' in entitySearchResponse['response'][0]:
                entityGuid = entitySearchResponse['response'][0]['props']['urn:lri:property_type:guid']
            # Create the entity if it doesn't already exist
            if entityGuid is None or len(entityGuid) == 0:
                entityGuid = self.entityCreate(entityId, str.format('urn:schema-org:entity_type:{0}', entityType), submitter)
            for key,propArray in entity['properties'].items():
                for prop in propArray:
                    if type(prop) == dict:
                        # Create child object
                        self.logging.debug(str.format('Creating child object, key: {0}, value: {1}', key, prop))
                        childEntityId = self.createEntity(prop, submitter)
                        self.createProperty(entityGuid, key, childEntityId, submitter)
                    elif type(prop) == str or type(prop) == unicode:
                        # Create normal property
                        self.createProperty(entityGuid, key, prop, submitter)
                    else:
                        self.logging.error(str.format('Unexpected property type, key: {0}, value: {1}, type: {2}', key, prop, type(prop)))
            return entityId
        except:
            self.logging.exception(str.format('entity: {0}', json.dumps(entity)))


    def createProperty(self, entityGuid, propName, propValue, submitter):
        try:
            officialPropName = self.makeOfficialPropertyName(propName)
            officialPropValue = propValue
            propertyTypeResponse = self.entitySearchById(officialPropName, True)
            if len(propertyTypeResponse['response']) == 0:
                # This gives us a more readable error in the log
                raise Exception('Property type "{0}" does not exist'.format(officialPropName))
            ranges = propertyTypeResponse['response'][0]['props']['urn:lri:property_type:ranges']
            # If the range of the property is an enumeration then make sure the enumeration and our enumeration value exist
            if ranges == 'urn:lri:entity_type:enumeration_member':
                enumerationId = self.makeEnumerationId(propName)
                officialPropValue = self.makeEnumerationValue(propName, propValue)
                self.createEnumerationValueIfNeeded(enumerationId, officialPropValue, propValue, submitter)
            self.propertyCreate(entityGuid, officialPropName, officialPropValue, submitter)
        except:
            self.logging.exception(str.format('entityGuid: {0} propName: {1} propValue: {2}', entityGuid, propName, propValue))


    def createEnumerationValueIfNeeded(self, enumerationId, enumerationValue, name, submitter):
        enumerationResponse = self.entitySearchById(enumerationId)
        if len(enumerationResponse['response']) == 0:
            self.entityCreate(enumerationId, 'urn:lri:entity_type:enumeration', 'LR_CONNECTOR') 
            enumerationResponse = self.entitySearchById(enumerationId)
        self.logging.debug('props: {0}'.format(enumerationResponse['response'][0]['props']))
        if 'urn:lri:property_type:has_enumeration_member' not in enumerationResponse['response'][0]['props'] or \
            (enumerationValue != enumerationResponse['response'][0]['props']['urn:lri:property_type:has_enumeration_member'] and \
            enumerationValue not in enumerationResponse['response'][0]['props']['urn:lri:property_type:has_enumeration_member']):
            enumerationValueEntityGuid = self.entityCreate(enumerationValue, 'urn:lri:entity_type:enumeration_member', submitter)
            self.propertyCreate(enumerationValueEntityGuid, 'urn:lri:property_type:name', name, submitter)
            self.propertyCreate(enumerationValueEntityGuid, 'urn:lri:property_type:is_member_of_enumeration', enumerationId, submitter)


    def makeEntityId(self, entityType, entity):
        entityIdTemplate = 'urn:schema-org:{0}:{{0}}:{{1}}'.format(entityType)
        if entityType == 'creative_work':
            return entityIdTemplate.format('url', helperfunctions.scrubUrl(entity['properties']['url'][0]))
        # AlignmentObject is unique.  It is essentially a hyperedge and is defined by the combination of its properties.
        if entityType == 'alignment_object':
            propCollection = ''
            for prop in self.alignmentObjectProperties:
                if prop in entity['properties']:
                    if isinstance(entity['properties'][prop], list) and \
                        len(entity['properties'][prop]) == 1 and \
                        (type(entity['properties'][prop][0]) == str or type(entity['properties'][prop][0]) == unicode):
                        propCollection += entity['properties'][prop][0]
                    else:
                        raise Exception('Unexpected property in AlignmentObject.  name: "{0}", value: "{1}"'.format(prop, entity['properties'][prop]))
                propCollection += '|'
            propCollection = propCollection[:-1]
            return entityIdTemplate.format('hash', hashlib.md5(propCollection).hexdigest())
        ''' Don't ever trust the id field coming in from the JSON
        if 'id' in entity and len(entity['id']) > 0:
            # id is specific to stand-alone schema.org JSON, if it starts with "urn:" then 
            # trust that it is properly formatted and globally unique
            if entity['id'].startswith('urn:'):
                return entity['id']
            return entityIdTemplate.format('id', entity['id'])
        '''
        for prop in self.potentialEntityIdProperties:
            if prop in entity['properties'] and \
                isinstance(entity['properties'][prop], list) and \
                len(entity['properties'][prop]) > 0 and \
                len(entity['properties'][prop][0]) > 0:
                value = entity['properties'][prop][0]
                if prop.lower().endswith("url"):
                    value = helperfunctions.scrubUrl(value)
                return entityIdTemplate.format(self.makeLowercaseUnderscore(prop), value)
        raise ValueError(str.format('unable to create entityId'))


    def makeLowercaseUnderscore(self, s):
        return re.sub("([a-z])([A-Z])","\\1_\\2",s).lower().lstrip('/')


    def makeOfficialPropertyName(self, propName):
        return str.format('urn:schema-org:property_type:{0}', self.makeLowercaseUnderscore(propName))


    def makeEnumerationId(self, propName):
        return str.format('urn:schema-org:enumeration:{0}', self.makeLowercaseUnderscore(propName))


    def makeEnumerationValue(self, propName, propValue):
        return str.format('urn:schema-org:enumeration_member:{0}:{1}', self.makeLowercaseUnderscore(propName), self.makeLowercaseUnderscore(propValue))


    def propertyCreate(self, entityGuid, propType, propValue, submitter):
        q = { \
            'from': entityGuid, \
            'proptype': propType, \
            'value': propValue \
        }
        opts = { \
            'access_token': self.config['lrib']['access_token'], \
            'on_behalf_of': submitter \
        }
        response = self.sendRequest('property', 'create', q, opts)
        if 'guid' not in response['response']:
            raise Exception('Guid not found in property/create response')
        return response['response']['guid']


    def entitySearchById(self, entityId, useCache = False):
        q = { \
            'urn:lri:property_type:id': entityId \
        }
        if useCache and \
            entityId in self.entityCache and \
            datetime.datetime.now() < (self.entityCache[entityId][0] + datetime.timedelta(seconds=self.config['lrib']['local_cache_expiration'])):
                return self.entityCache[entityId][1]
        response = self.sendRequest('entity', 'search', q)
        if useCache:
            self.entityCache[entityId] = [datetime.datetime.now(), response]
        return response


    def entityCreate(self, entityId, entityType, submitter):
        q = { \
            'urn:lri:property_type:id': entityId, \
            'urn:lri:property_type:types': [ \
                'urn:lri:entity_type:thing', \
                entityType \
            ] \
        }
        opts = { \
            'access_token': self.config['lrib']['access_token'], \
            'on_behalf_of': submitter \
        }
        response = self.sendRequest('entity', 'create', q, opts)
        if 'urn:lri:property_type:guid' not in response['response']:
            raise Exception('Guid not found in entity/create response')
        return response['response']['urn:lri:property_type:guid']


    def sendRequest(self, objectType, verb, q, opts = None):
        now = datetime.datetime.now()
        url = str.format('{0}/{1}/{2}?q={3}', self.config['lrib']['url'], objectType, verb, urllib.quote(json.dumps(q)))
        if opts is not None:
            url += str.format('&opts={0}', urllib.quote(json.dumps(opts)))
        self.logging.debug(str.format('LRIB Request: {0}', url))
        request = urllib2.Request(url)
        if 'username' in self.config['lrib'] and len(self.config['lrib']['username']) > 0 and \
            'password' in self.config['lrib'] and len(self.config['lrib']['password']) > 0:
            b64 = base64.encodestring(str.format('{0}:{1}', self.config['lrib']['username'], self.config['lrib']['password']))
            request.add_header("Authorization", str.format("Basic {0}", b64))
        response = json.load(urllib2.urlopen(request))
        if response is None:
            raise Exception('no response from LRIB')
        status = response['status'] if 'status' in response else ''
        message = response['message'] if 'message' in response else ''
        if status != 'normal':
            raise Exception('LRIB did not return "normal" status.  status: "{0}", message: "{1}"'.format(status, message))
        if 'response' not in response:
            raise Exception('"response" missing from LRIB response.  status: "{0}", message: "{1}"')
        self.logging.debug(str.format('LRIB Response: {0}', json.dumps(response)))
        return response
