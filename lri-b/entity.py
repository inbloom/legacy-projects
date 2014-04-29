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
import json,traceback,prop,copy,lrilog

# We won't try to validate our core schema
bootstrap_types=['type','property_type','property','data_type','key','namespace','thing']

class entity(object):
    
    def __init__(self,rec={},user=None,db=None,creator=None):

        self.user=user
        self.db=db
        self.jsondata=None
        self.props={}
        self.errors=[]
        self.invalid_properties={}
        self.is_valid=False
        self.guid=None
        self.creator=creator
        self.log = lrilog.lrilog("ENTITY")

        # Figure out what kind of initialization data we have
        self.rec=copy.deepcopy(rec)
        self.clean()
        self.parse_properties()
        if not self.errors:
            self.validate_properties()
        else:
            self.is_valid = False


    def clean(self):
        fieldnames=self.rec.keys()
        for f in fieldnames:
            if self.rec[f] in [[],{},None]:
                del self.rec[f]

        if "creator" in self.rec:
            self.creator = self.rec["creator"]
            del self.rec["creator"]

    def parse_json(self,jsondata):
        ''' Parse json for entity '''

        try:
            self.rec=json.loads(jsondata)
        except Exception, e:
            self.errors.append("JSON PARSE ERROR: "+traceback.format_exc())
            return False

        if not isinstance(self.props,dict):
            self.errors.append("JSON ENTITY INIT DATA IS NOT A DICTIONARY")
            return False

    def parse_properties(self):

        for k,vlist in self.rec.items():

            if not isinstance(vlist,list):
                vlist=[vlist]
            for v in vlist:
                proptype=self.db.schema.index["properties"].get(k,k)
                self.log.debug("PARSE_PROPERTIES: RENDERED PROP =",proptype,v,self.rec.get("urn:lri:property_type:guid",self.creator))
                p = prop.prop(entity=self,proptype=proptype,creator=self.creator,value=v,db=self.db,validate_entity=False)
                if p.is_valid:
                    self.log.debug("VALID PROPERTY:",k,p.rec)
                    if k not in self.props:
                        self.props[k]=[]
                    self.props[k].append(p)
                else:
                    self.log.debug("INVALID PROPERTY:",k,p.rec,p.errors)
                    self.errors.append("INVALID PROPERTY: "+repr(k))
                    self.errors.extend(p.errors)
                    if k not in self.invalid_properties:
                        self.invalid_properties[k]=[]
                    self.invalid_properties[k].append(p)

            self.log.debug("PARSED PROPERTIES IN INIT =\n",repr(dict([(k,[i.rec for i in v]) for k,v in self.props.items()])))
        


    def validate_properties(self):
        
        self.is_valid=False    

        if not self.rec.get('urn:lri:property_type:types'):
            self.errors.append('Entity is untyped.')
            return

        # Don't check our bootstrap schema
        self.log.debug("VALIDATE PROPS REC",self.rec)
        if 'urn:lri:property_type:id' in self.rec:
            ids = self.rec.get('urn:lri:property_type:id')
            if not isinstance(ids,list):
                ids=[ids]
            for i in ids:
                if i.replace('urn:lri:entity_type:','') in bootstrap_types:
                    self.is_valid=True
                    return True
        
        for k,plist in self.props.items():
            for p in plist:
                if not p.is_valid:
                    self.errors.append("Property "+str(k)+" is not valid because: "+json.dumps(p.errors))

        if not self.props.get('urn:lri:property_type:id'):
            self.errors.append("Missing urn:lri:property_type:id property.  Properties = "+repr(self.props.keys()))

        if not self.errors:
            self.is_valid=True

    def create(self):

        if self.errors:
            return False

        self.node = self.db.create_entity(creator=self.creator)

        if not self.node:
            self.errors.append("COULD NOT CREATE NODE IN DATABASE")
            return False

        # Set up our intrinsic node properties
        nodeprops={"urn:lri:property_type:guid":self.node["guid"],
                   "urn:lri:property_type:timestamp":self.node["timestamp"],
                   "urn:lri:property_type:creator":self.node["creator"]}

        self.log.debug("INTERNAL PROPERTIES",list(self.db.internal_properties(self.node)))
        rec = copy.deepcopy(self.db.internal_properties(self.node))
        self.log.debug("CREATED NODE =",rec)
        for k,v in nodeprops.items():
            self.rec[k]=v
            self.props[k] = [prop.prop(entity=self,proptype=k,creator=self.creator,value=v,db=self.db)]
        self.log.debug("\n\n\n\n\n\n\n\n NEW ENTITY PROPERTIES =",[(k,[i.rec for i in v]) for k,v in self.props.items()])

        # The properties we successfully create
        done_props = []

        # First do our id because we'll need that for the other properties
        if "urn:lri:property_type:id" in self.props:
            plist = self.props["urn:lri:property_type:id"]
        for p in plist:
            p.rec["from"]=rec["guid"]
            if not p.create(allow_nodeprops=True):
                self.errors.extend(["ENTITY ID CREATION FAILURE"]+p.errors)
                self.errors.append("FAILED TO CREATE PROPERTY: "+json.dumps(p.rec))
            else:
                done_props.append(p)

        if self.errors:
            # We failed to create our IDs so let's bail
            for dp in done_props:
                r = dp.delete()
                if not r:
                    self.errors.extend(dp.errors)
            #  Now let's delete our node
            self.errors.append("Destroying node '%s' "% (rec.get('guid')))
            self.delete()
            return False

        # Now we can do the rest of the properties
        for pname,plist in self.props.items():
            if pname != 'urn:lri:property_type:id':
                for p in plist:
                    p.rec["from"]=rec["guid"]
                    #if 'types' in pname:
                    #    self.log.debug("ZZZ CREATE TYPES PROP",pname,p.rec
                    if not p.create(allow_nodeprops=True):
                        self.errors.extend(p.errors)
                        self.errors.extend(["FAILED TO CREATE PROPERTY:",json.dumps(p.rec)])

                        for dp in done_props:
                            # We failed to create a property so fail the entire entity creation.
                            try:
                                dp.delete()
                            except Exception, e:
                                self.errors.extend(["Could not destroy link"]+traceback.format_exc().split("\n")) 

                        #  Now let's delete our node
                        self.delete()
                        self.errors.append("Destroying node '%s' "% (rec.get('guid')))
                        return False
                    
    def delete(self):
        # Really delete
        self.node.delete()
        



