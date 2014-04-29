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

immutable_props=["urn:lri:property_type:guid",
                 "urn:lri:property_type:timestamp",
                 "urn:lri:property_type:creator"]

class prop(object):


    def __init__(self,rec={},entity_guid=None,entity=None,creator=None,proptype=None,value=None,db=None,guid=None,validate_entity=True):

        self.db=db
        self.rec=copy.deepcopy(rec)
        self.errors=[]
        self.creator = creator
        self.invalid_fields={}
        self.is_valid=False
        self.link = None
        self.log = lrilog.lrilog("PROP")
        self.entity=entity
        if self.entity:
            self.entity_guid = self.entity.rec.get("urn:lri:property_type:guid")
        else:
            self.entity_guid = entity_guid

        if self.creator:
            self.rec["creator"] = self.creator

        self.log.debug("PROP INIT ENTITY GUID =",self.entity_guid,self.entity)
        
        # Extract our property name/value
        for k,v in self.rec.items():
            if k.startswith('urn:') and v != None: 
                self.rec['proptype'] = k
                self.rec['value'] = v


        self.guid=guid

        if guid:
            # prop exists, let's get it
            self.link = self.db.get_prop(guid)
            if self.link:
                for k,v in self.db.internal_properties(self.link).items():
                    if k != 'rec':
                        self.rec[k] = self.link[k]
                self.is_valid = True
            else:
                self.errors.append("Invalid property GUID.  Could not find.")
        elif proptype and value != None:
            self.log.debug("INIT FOR PROPERTY CREATE",entity,proptype,value,"\n\n\n")
            # we need to generate our fields and create our property
            self.rec["proptype"] = proptype
            self.rec["value"] = value
            self.prepare_for_creation()            
            self.validate_fields()
        elif 'guid' not in self.rec and 'proptype' in self.rec and ('value' in self.rec or 'to' in self.rec):
            self.prepare_for_creation()            
            self.validate_fields()
        else:
            self.errors.append("Not enough specification to find or create property.")
            

    def __str__(self):
        return json.dumps(self.rec)

    def parse_json(self,jsondata):
        ''' Parse json for property '''

        try:
            self.rec=json.loads(jsondata)
        except Exception, e:
            self.errors.append("JSON PARSE ERROR: "+traceback.format_exc())
            return False

        if not isinstance(self.rec,dict):
            self.errors.append("JSON PROPERTY INIT DATA IS NOT A DICTIONARY")
            return False

    def prepare_for_creation(self):
        
        if not self.rec["proptype"].startswith("urn:"):
            # Resolve our proper proptype
            self.rec["proptype"] = self.db.schema.index["id"].get(self.rec["proptype"],self.rec["proptype"])
        
        if not self.rec.get("from") and self.entity_guid:
            self.rec["from"] = self.entity_guid

        # Use default creator if needed
        if not self.creator:
            if 'creator' in self.rec:
                self.creator = self.rec['creator']
            else:
                self.creator = self.db.creator_guid
                self.rec['creator'] = self.creator

        return True

    def validate_fields(self):
        ''' Validate myself.  This is a very weak validation and should be improved.'''

        self.is_valid=False

        required_fields=['creator','proptype']

        for rf in required_fields:
            if not self.rec.get(rf):
                self.errors.append("Field '"+rf+"' is missing or empty.")
                return False # Missing field

        if self.rec.get("value") == None and self.rec.get("to") == None:
            self.errors.append("Fields 'value' and 'to' are both missing or empty.")
            return False # Missing field

        pt = self.rec.get('proptype')
        if not pt or pt not in self.db.schema.index['properties']:
            self.errors.append("Property %s does not seem to exist." % (repr(pt)))
            return False

        # get the schema for our proptype
        if not self.db.in_bootstrap:
            if not self.db.schema.index["id"].get(pt):
               self.errors.append("Property %s does not seem to exist." % (repr(pt))) 
               return False

            propkind = self.db.schema.property_target_kind(pt,in_bootstrap=self.db.in_bootstrap)
            if propkind == 'link':
                if 'value' in self.rec:
                    if not 'allow_bad_ids' in self.db.config:  # hideous hack for js
                        id_errors = self.db.problems_with_id(self.rec["value"])
                        if id_errors:
                            self.errors.extend(id_errors)
                            return False

        if self.db.in_bootstrap:
            self.is_valid = True
            return True

        ptrec = self.db.schema.index['id'].get(self.db.schema.index['properties'][pt])

        if 'urn:lri:entity_type:enumeration_member' in ptrec.get('urn:lri:property_type:ranges'):
            # Is enumerated value.  Let's make sure the value points
            # to an actual enumeratee
            if 'value' in self.rec:
                r = self.db.property_search({"value":self.rec['value'],
                                             "proptype":"urn:lri:property_type:id"})
                if r:
                    target_guid = r[0]['from']
                    eid = self.rec['value']
                else:
                    self.errors.append("Enumeration member %s does not seem to exist." % (repr(self.rec['value'])))
                    return False
                    
            elif 'to' in self.rec:
                target_guid = self.rec['to']
                eid = target_guid

            props = self.db.get_entity_properties(target_guid)['props']

            if 'urn:lri:entity_type:enumeration_member' in props['urn:lri:property_type:types'] or 'urn:lri:property_type:is_member_of_enumeration' in props:
                # Let's be generous-- either participation or types is good enough to be a valid enum member
                self.is_valid = True
                return True
            else:
                self.errors.append("Entity %s is not an enumeration member." % (repr(eid)))
                return False

        self.is_valid=True
        return True

    def create(self,is_update=False,allow_nodeprops=False):

        if self.errors:
            return False

        if not allow_nodeprops and self.rec.get("proptype") in immutable_props:
            self.errors.append("Creation of property type %s is not allowed." % (self.rec["proptype"]))
            return None

        if not self.rec.get("from"):
            if self.entity_guid:
                self.rec["from"] = self.entity_guid    
            else:
                self.errors.append("Entity GUID missing!. Cannot create.")
                return None


        if not self.errors:
            self.log.debug("PROP CREATE REC",self.rec)
            if self.entity:
                self.link = self.db.create_property(self.rec,
                                                    node=self.entity.node,
                                                    in_bootstrap=True,
                                                    is_update=is_update)
            else:
                self.link = self.db.create_property(self.rec,
                                                    in_bootstrap=True,
                                                    is_update=is_update)

            if not self.link:
                self.errors.extend(self.db.errors)
                self.log.debug("PROPERTY CREATION FAILURE BECAUSE:",self.db.errors)
                self.db.errors=[]
                return False

            for k,v in self.db.internal_properties(self.link).items():
                if k != 'rec':
                    self.rec[k] = v

        return True

    def update(self,newrec):

        if self.rec.get("proptype") in immutable_props:
            self.errors.append("Update of property type %s is not allowed." % (self.rec["proptype"]))
            return None
           
        
        if self.rec["replaced_by"] != "":
            self.errors.append("Property "+self.rec.get("guid")+" already updated.")
            return None

        if not self.rec.get("from"):
            self.errors.append("'from' field missing in existing property!  Cannot update")
            return None
        
        # Make sure the update is idempotent
        if "to" in newrec and "to" in self.rec:
            if newrec["to"] == self.rec["to"]:
                self.errors.append("Can't update property with same 'to' field.")
                return None
        elif "value" in newrec and "value" in self.rec:
            if newrec["value"] == self.rec["value"]:
                self.errors.append("Can't update property with same 'value' field.")
                return None
        elif "value" in newrec and "to" in self.rec:
            to_guids = self.db.get_guids(newrec["value"])
            if to_guids:
                if to_guids[0] == self.rec["to"]:
                    self.errors.append("Can't update property with same target.")
                    return None
                newrec["to"] = to_guids[0]
                del newrec["value"]
        elif "to" in newrec and "value" in self.rec:
            if self.rec["complete"] == False:
                # Could be manual property completion
                if "value" in newrec:
                    del newrec["value"]
            else:
                # Can't have 'to' in literal property
                self.errors.append("Literal property cannot be updated to link property.")
                return None
                

        if not self.errors:
            self.rec['internal'] = self.link
            self.log.debug("IN PROP UPDATE -- OLDREC ",self.rec)
            self.log.debug("IN PROP UPDATE -- NEWREC ",newrec)
            return self.db.update_property(oldrec=self.rec,newrec=newrec)

    def delete(self):
        # Really delete
        #self.log.debug("\n\nDELETING LINK: %s \n\n" % (str(self.rec))
        self.link.delete()
        



           
            
