#!/usr/bin/env python
# Copyright 2012-2013 inBloom, Inc. and its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json,sys,httplib2,urllib,yaml,traceback,copy,base64,zlib

def parse_cursor(s):
    return(json.loads(zlib.decompress(base64.urlsafe_b64decode(s.encode('utf-8')))))

class client(object):

    def __init__(self,host='127.0.0.0',port=8000,verbose=False):
        self.headers={}
        self.host=host
        self.port=port
        self.verbose=verbose
        self.errors = []
        self.connect()

    def connect(self):
        try:
            self.conn=httplib2.Http()
        except:
            self.errors.append("Failed to connect to server at host %s port %s." % (self.host,self.port))
            if self.verbose:
                print self.errors[-1]

    #def query(self,httpmode,command,q,opts,parse=True):
    def query(self, *args, **kwargs):
        if not kwargs:
            parse = True
        else:
            parse = kwargs['parse']
        if len(args) == 4:
            httpmode, command, q, opts = args[0:4]
        elif len(args) == 3:
            httpmode, command, q, opts = 'GET', args[0], args[1], args[2]
        uq=urllib.urlencode({"q":json.dumps(q)})
        uopts=urllib.urlencode({"opts":json.dumps(opts)})
        if httpmode == 'GET':
            url='http://'+self.host+':'+str(self.port)+'/'+command+'?'+uq+'&'+uopts
            resp,cont=self.conn.request(url,method='GET',headers=self.headers)
        elif httpmode == 'POST':
            url='http://'+self.host+':'+str(self.port)+'/'+command
            resp,cont=self.conn.request(url,method='POST',headers=self.headers,body='?'+uq+'&'+uopts)
        else:
            print "BAD HTTP MODE:",httpmode
            return None
            
        if self.verbose:
            print "REQUEST URL =",url
        if resp.status==200:
            if not parse:
                return cont
            if not opts.has_key("format") or opts["format"] == "json":
                j=json.loads(cont)
                return j
            elif opts.has_key("format"):
                if opts["format"] == "yaml":
                    return yaml.safe_load(cont)
                elif opts["format"] in ["xml","oldxml","johnxml"]:
                    return cont
        else:
            print resp,cont
        return None

    def search_iter(self,q,opts={},pagesize=10):
        opts['format'] = 'json'
        lq = copy.deepcopy(q)
        lq['limit'] = pagesize
        r = self.query('POST','entity/search',lq,opts)
        hits = []
        if r.get('response'):
             hits.extend(r['response'])
        find_dupes(hits)
        while r.get('cursor'):
            #print "ITER CURSOR:",r['cursor'][0:60]
            #print "DECODED CURSOR:",json.dumps(parse_cursor(r['cursor']),indent=4,sort_keys=True)
            lq = {"cursor":r['cursor'],"limit":pagesize}
            r = self.query('POST','entity/search',lq,opts)
            if r.get('response'):
                hits.extend(r['response'])
            print "TOTAL HITS:",len(hits)
            find_dupes(hits)
        return hits
                     

def find_dupes(l):
    h = set()

    for hit in l:
        i = hit['props']['urn:lri:property_type:guid']
        if i in h:
            print "DUPLICATE! ",i
        h.add(i)

    #print "TOTAL SET:",json.dumps(sorted(list(h)),indent=4)
        
if __name__=='__main__':
    h,p = sys.argv[1].split(":")
    c=client(host=h,port=int(p))
    q = json.loads(sys.argv[2])
    print "QUERY:\n",json.dumps(q,indent=4,sort_keys=True)
    if len(sys.argv) > 3:
        pagesize = sys.argv[3]
    else:
        pagesize,pagesize = 10

    response = c.search_iter(q,pagesize=pagesize)
    print json.dumps(response,indent=4,sort_keys=True)


"""    
Usage examples:\n
./client.py GET entity/search '{"urn:lri:property_type:types":"urn:lri:entity_type:type"}' '{"details":true}'
./client.py GET entity/create '{"urn:lri:property_type:id":"MY_FQGUID","urn:lri:property_type:types":["urn:lri:entity_type:thing"]}' 
./client.py GET property/create '{"from":"MY_ENTITY_GUID","urn:lri:property_type:name":"THE NAME OF MY ENTITY"}' 
./client.py GET property/update '{"guid":"MY_PROPERTY_GUID","value":"MY NEW NAME"}' 

"""



