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
import json,datetime,traceback,httplib,cache,sys

default_slc_server = 'api.sandbox.inbloom.org'
default_url_path = '/api/rest/system/session/check'

default_ttl = 900  # Every 15 mins we check again

def make_user_id_urn(s):
    return "urn:inbloom:user:"+s

class user(object):

    def __init__(self,access_token='',slc_server=default_slc_server,admin_access_tokens={},
                 delegate_tokens=[],url_path=default_url_path,cache=None,ttl=default_ttl):
        self.access_token = access_token
        self.admin_access_tokens = admin_access_tokens
        self.delegate_tokens = delegate_tokens
        self.state = 'PENDING'
        self.slc_server = slc_server
        self.url_path = url_path
        self.cache = cache
        self.headers = {'Authorization':'bearer '+access_token}
        self.resp = {}
        self.id = ''
        self.realm = ''
        self.authenticated_by = None
        self.errors = []

    def __str__(self):
        return json.dumps({"access_token":self.access_token,
                           "admin_access_tokens":self.admin_access_tokens,
                           "delegate_tokens":self.delegate_tokens,
                           "state":self.state,
                           "id":self.id,
                           "errors":self.errors,
                           "resp":self.resp})

    def authenticate(self):
        if not self.access_token:
            self.errors = ['Empty Access Token']     
            return False
    
        if self.authenticate_admin():
            return True
            self.authenticated_by = 'ADMIN'
        else:
            return self.authenticate_slc()

    def authenticate_admin(self,admin_access_tokens={}):
        self.id = self.admin_access_tokens.get(self.access_token,'')
        if self.id:
            return True
        return False
  
    def authenticate_slc(self):
        self.timestamp = datetime.datetime.utcnow().isoformat()
        data = None

        print 'GET',self.url_path,'',self.headers
        try:
            conn = httplib.HTTPSConnection(self.slc_server)
            req = conn.request('GET',self.url_path,'',self.headers)
            r = conn.getresponse()
            data = r.read()
        except Exception, e:
            self.errors = ["UNABLE TO CONNECT TO AUTHORIZATION SERVER!",
                           "inBloom request:",repr(self.url_path),"headers:",json.dumps(self.headers),"inBloom raw response:",repr(data)]
            self.state = 'ERROR'
            return False
        try:
            self.resp = json.loads(data)
        except Exception, e:
            self.errors = ["BAD JSON RESPONSE FROM AUTHORIZATION SERVER!",
                           "inBloom request:",repr(self.url_path),"headers:",json.dumps(self.headers),"inBloom raw response:",repr(data)]
            self.errors.extend(traceback.format_exc().split("\n"))
            self.state = 'ERROR'
            return False

        if self.resp.get('authenticated') == True:
            self.state = 'AUTHENTICATED'
            if self.parse() and self.cache:
                self.cache.write_pair(make_user_id_urn(self.id),datetime.datetime.utcnow().isoformat())
                return True
            else:
                return False
        else:
            self.errors = ["UNPARSEABLE RESPONSE FROM AUTHORIZATION SERVER!",
                           "inBloom request:",repr(self.url_path),"headers:",json.dumps(self.headers),"inBloom raw response:",repr(data)]
            self.errors.extend(["Authentication failure"])
             
            self.state = 'INVALID'
            return False
            
    def parse(self):

        self.realm = self.resp.get('realm')
        self.user_id = self.resp.get('user_id')
        print self.realm

        if self.realm and self.user_id:
            self.state = 'PARSED'
            self.id = 'urn:inbloom:user:%s:%s' % (self.realm,self.user_id)
            self.authenticated_by = 'inBloom'
            return True
        self.errors = ['Unable to parse inBloom authentication response: '+repr(self.resp)]
        return False

    def __str__(self):
        return self.id
            
def test(access_token=''):
    u = user(access_token=access_token)
    u.authenticate()
    print "HTTP RESPONSE:",u.resp
    print "        STATE:",u.state
    print "        REALM:",u.realm
    print "           ID:",u.id
  
if __name__=='__main__':
    if len(sys.argv) >1:
        test(access_token=sys.argv[1])
    else:
        test()
        
        
'''
{"authenticated":true,"edOrg":null,"edOrgId":null,"email":"junk@junk.com","external_id":"linda.kim","full_name":"Mrs Linda Kim","granted_authorities":["Educator","Educator"],"realm":"45b01db0-1bed-6dd7-a936-09ab31bd37fe","rights":["AGGREGATE_READ","READ_PUBLIC","READ_GENERAL"],"sliRoles":["Educator","Educator"],"tenantId":"kurt@bollacker.com","user_i
'''
    
'''
To get an access token:
https://slc.tearnen.net/
Go

zAUDEZJw3z
95UPN8sog6b7SSFptOvhAUFoicpLP9q3O9AdxoStfl8KvcwJ
api.sandbox.slcedu.org
v1
'''
