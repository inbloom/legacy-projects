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
import traceback,datetime,json,yaml,entity,prop,copy,timer,cache,user
import os.path
import xml.dom.minidom
import xml.etree.ElementTree
default_version = "0.5"

response_envelope_template = {"status":"normal",
                              "api_version":default_version,
                              "q":{},
                              "opts":{}}

class request(object):

    def __init__(self,action=None,q={},opts={},db=None,ext_cache=None):

        self.action = action
        self.q = q
        self.opts = opts
        self.db = db
        self.cache = ext_cache
        self.user = None
        self.r=copy.deepcopy(response_envelope_template)
        self.errors = []

    def authenticate_user(self):
        #return True
        if self.db:
            # First check for delegation backdoor
            if self.opts.get('on_behalf_of') and self.opts.get("access_token") in self.db.config.get('delegate_tokens'):
                self.user = user.user(cache = self.cache)
                self.user.id = self.opts['on_behalf_of']
                return True
            else:
                # Must be normal or admin access_token
                self.user = user.user(access_token = self.opts.get("access_token",""),
                                      #slc_server = self.db.config.get("slc_server_host",user.default_slc_server),
                                      #url_path = self.db.config.get("slc_token_check_path",user.default_url_path),
                                      admin_access_tokens = self.db.config.get("admin_access_tokens",{}),
                                      delegate_tokens = self.db.config.get("delegate_tokens",[]),
                                      cache = self.cache)
                #print "USER STR",self.user,":",self.user.access_token,":",self.opts,":",self.opts.get("access_token",""),":"
                return self.user.authenticate()
        self.errors.append("No DB connection.  Cannot authenticate user.")
        return False   

    def is_schema_write(self):

        # For entity/create
        ts = self.q.get("urn:lri:property_type:types",[])
        if ts:
            if not isinstance(ts,list):
                ts=[ts]
            for t in ts:
                if t in ["urn:lri:entity_type:type","urn:lri:entity_type:datatype","urn:lri:entity_type:property_type"]:
                    # We're trying to add a type to an entity
                    return True

        # For property/create and property/update
        f = self.q.get("from")
        # All schema properties are outgoing
        if f in self.db.schema.index["guid"]:
            return True

        return False
        

    @timer.timer("perform_request")
    def perform_request(self):
        before = datetime.datetime.utcnow()
        self.r["timestamp"] = before.isoformat()
        self.r["q"] = self.q
        self.r["opts"] = self.opts
        self.r["action"] = self.action
        
        if not self.q or self.opts == False:
             self.bad_query()
  
        success = False

        if self.action in ['entity/create','property/create','property/update']:
            print "IS SCHEMA WRITE:",self.is_schema_write()
            if not self.authenticate_user():
                print "FAILED TO AUTHENTICATE USER",self.errors,":",self.user.errors
                self.bad_user()
            elif self.is_schema_write() and self.user.id not in self.user.admin_access_tokens.values():
                self.errors.append("Only administrative accounts can edit schema.")
                self.r["status"] = "error"
                self.r["message"] = self.errors

        if not self.errors:

            # Set our creator for writes
            if self.user:
                self.r["authenticated_creator_id"] = self.user.id
                # self.db.creator_guid = self.user.id


            # Clear previous DB errors.
            self.db.errors = []
        
            try:
                if self.action == 'entity/search':
                    success = self.entity_search()
                elif self.action == 'entity/create':
                    success = self.entity_create()
                    self.clear_cache()
                elif self.action == 'property/create':
                    success = self.property_create()
                    self.clear_cache()
                elif self.action == 'property/update':
                    success = self.property_update()
                    self.clear_cache()
                elif self.action == 'db/shutdown':
                    success = self.shutdown()
                else:
                    self.unknown_action()
                self.http_status = "200 OK"
            except Exception, e: 
                self.errors.extend(["ARG! INTERNAL ERROR! DUMP:"]+traceback.format_exc().split("\n"))

                self.http_status = "500 Internal Server Error"
                self.r["status"] = "error"
                self.r["message"] = self.errors
                success = False

        # Remove duplicate error message lines
        if self.r.get("message"):
            elist = []
            for e in self.r["message"]:
                if not elist or elist[-1] != e:
                    elist.append(e)
            self.r["message"] = elist
        
        after = datetime.datetime.utcnow()
        self.r["query_seconds"] = (after - before).total_seconds()
        return success

    @timer.timer("response_string")
    def response_string(self,format="json"):

        # Let's see if we've already cached the rendered result
        #result_hash=format+":"+json.dumps(self.q)
        #if format in rcache and result_hash in rcache[format] and self.opts.get("use_cached") != False:
        #    return rcache[format][result_hash]
            
        if format=='json':
            result = json.dumps(self.r,indent=4,sort_keys=True)
        elif format=='yaml':
            result = yaml.dump(self.r,default_flow_style=False).replace("!!python/unicode","")
        elif format == 'xml':
            result = render_xml(self.r).encode('utf-8')
        elif format == 'johnxml':
            result = render_john_xml(self.r).encode('utf-8')
        else:
            return "UNKNOWN FORMAT:"+repr(format)

        #rcache[format][result_hash] = result

        return result
        
    def entity_search(self):
        
        cache_key = cache.make_key([self.q,self.opts.get("details")])
        print "\n\n\n\n\nCACHEKEY:",cache_key

	cache_result = None
	if self.cache and self.opts.get("use_cached") != False:
	    cache_result  = self.cache.read(cache_key)
	    
        if cache_result:
            self.r["response"] = cache_result["value"]["response"]
            self.r["cursor"] = cache_result["value"]["cursor"]
	    self.r["time_cached"] = cache_result["timestamp"]
            self.r["cached"] = True
        else:
            resp = self.db.entity_search(self.q,include_internal_objects=False,include_details=self.opts.get("details",False),get_history=self.opts.get("get_history",False))
            self.r["response"] = resp['entities']
            self.r["cursor"] = resp['cursor']
            if self.db.errors:
                self.r["status"]="error"
                self.r["message"]=self.db.errors
                self.db.errors = [] 
                return False
   	    if self.cache:
                self.cache.write_pair(cache_key,{"response":self.r["response"],"cursor":self.r["cursor"]})
            self.r["cached"] = False
        return True
    
    def entity_create(self):
        e = entity.entity(rec=self.q,db=self.db,creator=self.user.id)
        if e.errors:
            self.r["status"]="error"
            self.r["message"]=e.errors
            return False
        else:
            e.create()
            if e.errors:
                self.r["status"]="error"
                self.r["message"]=e.errors
                return False
            else:
                self.r["response"] = e.rec
                return True 

    def property_create(self):
        p = prop.prop(rec=self.q,db=self.db,creator=self.user.id)
        p.create()
        if p.errors:
            self.r["status"]="error"
            self.r["message"]=p.errors
            return False
        else:
            self.r["response"] = p.rec
            return True

    def property_update(self):
            if "guid" not in self.q:
                self.r["status"]="error"
                self.r["message"]=["'guid' field missing from query"]
                return False
            else:
                p = prop.prop(guid=self.q.get("guid"),db=self.db,creator=self.user.id)
                if p.is_valid:
                    newrec={}
                    for f in ['value','to','from','alive','complete','proptype']:
                        if f in self.q:
                            newrec[f]=self.q[f]
                    newp = p.update(newrec)
                    if newp:
                        if newp.errors:
                            self.r["status"]="error"
                            self.r["message"]=newp.errors
                            return False
                        else:
                            p = prop.prop(guid=p.rec["guid"],db=self.db)
                            self.r["response"] = {"old":p.rec,"new":newp.rec}
                            return True
                    else:
                        self.r["status"]="error"
                        self.r["message"]=["Unable to create updated property object. "+(" ".join(p.errors))+(" ".join(self.db.errors))]
                        return False
                        
                else:
                    self.r["status"]="error"
                    self.r["message"]=p.errors
                    return False

    '''
    def shutdown(self):
        if self.opts.get("admin_passwd") and self.opts.get("admin_passwd") == self.admin_passwd:
            self.db.close()
            self.r["response"] = {}
            self.r["status"]="normal"
            self.r["message"]="Server Shut Down"
            return True
        else:
            self.r["status"]="error"
            self.r["message"]="Incorrect Password"
            return False
    '''
	    
    def unknown_action(self):
        self.r["status"]="error"
        self.r["message"]=["Unknown action: "+repr(self.action)]
        return False

    def bad_query(self):
        self.r["status"]="error"
        self.http_status = "400 Bad Request"
        self.r["message"]=["Bad query: q="+repr(self.q)+" opts="+repr(self.opts)]
        return False

    def bad_user(self):
        self.r["status"]="error"
        self.r["message"]=["Unable to confirm access token: "+repr(self.opts.get("access_token"))]
        self.errors += self.user.errors
        self.r["message"] += self.errors
        self.http_status = "401 Unauthorized"
        return False

    def clear_cache(self):
	if self.cache:
            self.cache.clear()

def render_john_xml(x,indent="",tagname="",depth=0):
    s=[]

    first = False
    if indent == "":
        first = True

    if first:
        s.append("<?xml version=\"1.0\" ?>\n\n<root>\n")
        indent="  "

    if isinstance(x,list):
        for y in x:
            if isinstance(y,list) or isinstance(y,dict):
                s.append(indent+"<value>\n")
                s.append("%s" % (render_john_xml(y,indent=indent+"  ",depth=depth+1)))
                s.append(indent+"</value>\n")
            else:
                try:
                    s.append(indent+"<value>%s</value>\n" % (str(y)))
                except:
                    s.append(indent+"<value>%s</value>\n" % (repr(y)))
    elif isinstance(x,dict):
        for k,v in x.items():
            s.append(indent+"<pair key=\"%s\">\n" % (k))
            if not isinstance(v,list):
                v=[v]
            s.append(render_john_xml(v,indent=indent+"  ",depth=depth+1))
            s.append(indent+"</pair>\n")

    if first:
        s.append("</root>")

    return("".join(s))

def render_xml(x,indent="",tagname="",depth=0):
    s=[]

    first = False
    if indent == "":
        first = True

    if first:
        s.append("<?xml version=\"1.0\" ?>\n\n<root>\n")
        indent="  "

    if isinstance(x,list):
        for y in x:
            if isinstance(y,list) or isinstance(y,dict):
                s.append(indent+"<value>\n")
                s.append("%s" % (render_xml(y,indent=indent+"  ",depth=depth+1)))
                s.append(indent+"</value>\n")
            else:
                try:
                    s.append(indent+"<value>%s</value>\n" % (str(y)))
                except:
                    s.append(indent+"<value>%s</value>\n" % (repr(y)))
    elif isinstance(x,dict):
        for k,v in x.items():
            s.append(indent+"<pair>\n")
            s.append(indent+"  <key>%s</key>\n" % (k))
            if not isinstance(v,list):
                v=[v]
            s.append(render_xml(v,indent=indent+"  ",depth=depth+1))
            s.append(indent+"</pair>\n")

    if first:
        s.append("</root>")

    return("".join(s))

