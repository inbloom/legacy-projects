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
import sys,json,re,traceback

def fix_id(i,obj_type,namespace='lri'):
    # Convert to lowercase 
    if i.startswith('urn:'):
        return i
    return 'urn:'+namespace+':'+obj_type+':'+re.sub("([a-z])([A-Z])","\\1_\\2",i).lower()  

literal_names = ["Text","URL","URN","Integer","Float","Boolean","datetime","guid","Number"]
entity_names = ["Organization"]
quantity_names = ["Quantity","Duration","Distance","Energy","Mass"]

class org2lri(object):

    def __init__(self,infile):
        self.infile = infile
        self.s={'datatypes':{},
                'types':{},
                'properties':{}}
        self.name={'datatypes':{},
                   'types':{},
                   'properties':{}}

        self.errors=[]
        self.warns=[]
    
    def load_schema_file(self):
        # Load from file
        try:
            with open(self.infile) as fh:
                self.s = json.loads(fh.read())
                return True
        except Exception, e:
            self.errors.append("JSON PARSE ERROR FROM FILE: "+repr(self.infile)+"  "+traceback.format_exc())
            print self.errors
            return False

    def process_loaded_schema(self,in_bootstrap=False,db=None):

        # Do some internal indexing

        pathmap={'datatypes':'data_type',
                 'types':'entity_type',
                 'properties':'property_type'}

        # Quantities should be datatypes
        for q in quantity_names:
            if q in self.s['types']:
                del self.s['types'][q]
                print "Deleted Quantity Type:",q

        for objecttype in ["datatypes","types","properties"]:
            for tname,t in self.s.get(objecttype,{}).items():
                print "PROCESSING",objecttype,tname

                if objecttype == 'datatypes':
                    tid = fix_id(tname,pathmap[objecttype],namespace="lri")
                    self.name[objecttype][tname] = tid

                # Delete redundant fields
                if 'comment' in t:
                    del t['comment']
                if objecttype == 'types':
                    if 'subtypes' in t:
                        del t['subtypes']
                    if 'ancestors' in t:
                        del t['ancestors']
                    if 'properties' in t:
                        del t['properties']

                    if 'instances' in t:
                        del t['instances']

                    if tname.lower() != "thing":
                        tid = fix_id(tname,pathmap[objecttype],namespace="schema-org")
                    else:
                        tid = fix_id(tname,pathmap[objecttype],namespace="lri")
                    t['urn:lri:property_type:id'] = tid
                    del t['id']
                    self.s[objecttype][tid] = t
                    #del self.s[objecttype][tname] 

                    # Index tid by its original name
                    self.name[objecttype][tname] = tid


                    fixed_supertypes = []
                    for i in t['supertypes']:
                        if i.lower() != 'thing':
                            fixed_supertypes.append(fix_id(i,'entity_type',namespace='schema-org'))
                    t['supertypes'] = fixed_supertypes

                    fixed_specificprops = []
                    for i in t['specific_properties']:
                        if i in self.s['properties']:
                            fixed_specificprops.append(fix_id(i,'property_type',namespace='schema-org'))
                        else:
                            fixed_specificprops.append(fix_id(i,'property_type',namespace='lri'))
                    t['specific_properties'] = fixed_specificprops
                    



                # Make all properties inside schema be fully qualified
                for k,v in t.items():
                    if not k.startswith("urn:"):
                        fk= fix_id(k,'property_type')
                        t[fk] = v
                        del t[k]

                # Fix our handle and id
                if objecttype == 'properties':
                        
                    tid = fix_id(tname,pathmap[objecttype],namespace="schema-org")
                    t['urn:lri:property_type:id'] = tid
                    self.s[objecttype][tid] = t
                    del self.s[objecttype][tname] 

                    # Index tid by its original name
                    self.name[objecttype][tname] = tid


                    # Default properties to primary, not mandatory, not unique
                    if 'urn:lri:property_type:is_primary' not in t:
                        t['urn:lri:property_type:is_primary'] = True
                    if 'urn:lri:property_type:mandatory' not in t:
                        t['urn:lri:property_type:mandatory'] = False
                    if 'urn:lri:property_type:is_unique' not in t:
                        t['urn:lri:property_type:is_unique'] = False

                    if not t.get('urn:lri:property_type:ranges'):
                        print "BAD RANGE:",t
                    if not t.get('urn:lri:property_type:domains'):
                        print "BAD DOMAIN:",t

                    # Correct our domain and range values
                    fixed_domains = []
                    fixed_ranges = []
                    #print json.dumps(t,indent=4,sort_keys=True)

                    for i in t['urn:lri:property_type:ranges']:
                        if i in self.name['types']:
                            if i.lower() != 'thing':
                                fixed_ranges.append(fix_id(i,'entity_type',namespace='schema-org'))
                            else:
                                fixed_ranges.append(fix_id(i,'entity_type',namespace='lri'))
                        elif i in self.name['datatypes'] or i in literal_names+quantity_names:
                            fixed_ranges.append(fix_id(i,'data_type',namespace='lri'))
                        elif i.startswith("urn:"):
                            fixed_ranges.append(i)
                        else:
                            print "BAD RANGE VALUE:",i,json.dumps(t,indent=4,sort_keys=True)
                            print self.name['datatypes'].keys()

                    for i in t['urn:lri:property_type:domains']:
                        if i in self.name['types'] and i.lower() != 'thing':
                            fixed_domains.append(fix_id(i,'entity_type',namespace='schema-org'))
                        else:
                            fixed_domains.append(fix_id(i,'entity_type',namespace='lri'))

                    t['urn:lri:property_type:domains'] = fixed_domains
                    t['urn:lri:property_type:ranges'] = fixed_ranges

        for t in self.s['types'].keys():
            if not t.startswith("urn:"):
                del self.s['types'][t]
                
                    
    def save_schema_file(self):
        try:
            fh = open(self.infile.replace('.json','_fixed.json'),'w')
            fh.write(json.dumps(self.s,indent=4,sort_keys=True))
            fh.close()
            return True
        except Exception, e:
            self.errors.append("WRITE ERROR TO FILE: "+repr(self.infile.replace('.json','_fixed.json'))+"  "+traceback.format_exc())
            return False

    def run(self):
        self.load_schema_file()
        self.process_loaded_schema()
        del self.s['datatypes'] # We're not going to use schema.org's datatypes or "Thing"
        if 'urn:lri:entity_type:thing' in self.s['types']:
            del self.s['types']['urn:lri:entity_type:thing']
        self.save_schema_file()

if __name__=='__main__':
    o2l = org2lri(sys.argv[1])
    o2l.run()
                            
                            
