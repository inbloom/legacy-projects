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
import json,traceback,copy,entity,prop,re,lrilog

literals=["description","guid","id","image","name","timestamp","url","text",
          "comment","comment_plain","uri","label","creator","is_unique",
          "is_primary","mandatory","value","rank","alive"]

primaries=["supertypes","types","ancestors","properties","specific_properties","domains","ranges","reverse"]

default_bootstrap_file="./bootstrap.json"

# Convenience global variable
guid_to_id={}


def fix_id(i,obj_type):
    # Convert to lowercase id names with _ instead of caps as separator
    if i.startswith('urn:'):
        return i
    return 'urn:lri:'+obj_type+':'+re.sub("([a-z])([A-Z])","\\1_\\2",i).lower() 


class schema(object):

    def __init__(self,bootstrap_filenames=[default_bootstrap_file],in_test_mode=False,creator=None):
        self.s={'datatypes':{},
                'types':{},
                'properties':{}}
        self.index={'datatypes':{},
                    'types':{},
                    'properties':{},
                    'id':{},
                    'guid':{}}
        self.creator = creator
        self.log = lrilog.lrilog("SCHEMA")
        global guid_to_id
        guid_to_id = self.index["guid"]

        self.errors=[]
        self.warns=[]
        self.bootstrap_filenames=bootstrap_filenames
        self.in_test_mode = in_test_mode

    def load_bootstrap(self):
        for filename in self.bootstrap_filenames:
            self.load_schema_file(filename)
        if not self.errors:
            self.process_loaded_schema(in_bootstrap=True)
            self.log.debug("BOOTSTRAP SUCCESSFULLY LOADED")
        else:
            self.log.debug(repr(self.errors))

    def load_schema_file(self,filename):
        # Load from file
        try:
            with open(filename) as fh:
                s = json.loads(fh.read())
        except Exception, e:
            self.errors.append("JSON PARSE ERROR FROM FILE: "+repr(filename)+"  "+traceback.format_exc())
            return None

        self.merge_loaded_schema(s)

    def merge_loaded_schema(self,s):

        for ot in ["datatypes","types","properties"]:
            if ot in s:
                for k,v in s[ot].items():
                    if k not in self.s[ot]:
                        self.s[ot][k]=v
                    else:
                        self.warns.append("Type already loaded :"+json.dumps(v))


    def process_loaded_schema(self,in_bootstrap=False,db=None):

        # Do some internal indexing

        pathmap={'datatypes':'data_type',
                 'types':'entity_type',
                 'properties':'property_type'}

        for objecttype in ["datatypes","types","properties"]:
            for tname,t in self.s.get(objecttype,{}).items():

                # Make all properties inside schema be fully qualified
                for k,v in t.items():
                    if not k.startswith("urn:"):
                        fk= fix_id(k,'property_type')
                        t[fk] = v
                        del t[k]

                # Fix our handl and id
                fixed_tname=fix_id(tname,pathmap[objecttype])
                #self.log.debug(t)
                t['urn:lri:property_type:id']=fix_id(t['urn:lri:property_type:id'],pathmap[objecttype])

                if t["urn:lri:property_type:id"] in self.index["id"]:
                    self.log.debug(t["urn:lri:property_type:id"],"TYPE ALREADY IN INDEX AS",pathmap[objecttype])
                    continue
                self.index["id"][t["urn:lri:property_type:id"]]=t

                if tname not in self.index[objecttype]:  # Don't clobber existing
                    self.index[objecttype][tname]=t["urn:lri:property_type:id"]
                if fixed_tname not in self.index[objecttype]:  # Don't clobber existing
                    self.index[objecttype][fixed_tname]=t["urn:lri:property_type:id"]

                else:
                    self.log.debug(tname,"ALREADY IN INDEX",self.index[objecttype][tname])

                # Default properties to primary.
                if objecttype == 'properties' and 'urn:lri:property_type:is_primary' not in t:
                    t['urn:lri:property_type:is_primary'] = True
                    

        # Correct the "id"s in properties (supertypes/ranges/id) 
        # that simply refer to a schema.org name or are a retrieved 
        # internal GUID

        for tid,t in self.index["id"].items():
            self.log.debug("WORKING ON",tid)
            for f in ["urn:lri:property_type:supertypes","urn:lri:property_type:ranges"]:
                new=[]
                tvals = t.get(f,[])
                if not isinstance(tvals,list):
                    tvals=[tvals]
                for tname in tvals:
                    #self.log.debug(f,tname,json.dumps(t))
                    if re.match("[\da-z]{32}",tname):
                        # Must be GUID --- will never happen in_test_mode
                        tname = db.get_best_id(tname,in_bootstrap=True)
                        new.append(tname)
                    elif not tname.startswith("urn:"):
                        tname = fix_id(tname,'entity_type')
                        if "entity_type" in t["urn:lri:property_type:id"]:
                            new.append(self.index["types"][tname])
                    else:
                        new.append(tname)
                t[f] = new


        # Remove subtypes -- they are redundant
            if "urn:lri:property_type:subtypes" in t:
                del t["urn:lri:property_type:subtypes"]

        # Add appropriate "types" property for each schema,  Don't clobber existing types
        for tid in self.index["datatypes"].values():
            t = self.index["id"][tid]
            if not t.get("urn:lri:property_type:types"):
                t["urn:lri:property_type:types"] = ["urn:lri:entity_type:data_type"]
            else: 
                if not isinstance(t["urn:lri:property_type:types"],list):
                    t["urn:lri:property_type:types"] = [t["urn:lri:property_type:types"]]
                t["urn:lri:property_type:types"].append("urn:lri:entity_type:data_type")
                t["urn:lri:property_type:types"] =list(set(t["urn:lri:property_type:types"]))
        for tid in self.index["types"].values():
            t = self.index["id"][tid]
            if not t.get("urn:lri:property_type:types"):
                t["urn:lri:property_type:types"] = ["urn:lri:entity_type:type"]
            else: 
                if not isinstance(t["urn:lri:property_type:types"],list):
                    t["urn:lri:property_type:types"] = [t["urn:lri:property_type:types"]]
                t["urn:lri:property_type:types"].append("urn:lri:entity_type:type")
                self.log.debug("TYPING OBJECT:", t)
                t["urn:lri:property_type:types"] =list(set(t["urn:lri:property_type:types"]))
        for tid in self.index["properties"].values():
            t = self.index["id"][tid]
            if not t.get("urn:lri:property_type:types"):
                t["urn:lri:property_type:types"] = ["urn:lri:entity_type:property_type"]
            else: 
                if not isinstance(t["urn:lri:property_type:types"],list):
                    t["urn:lri:property_type:types"] = [t["urn:lri:property_type:types"]]
                t["urn:lri:property_type:types"].append("urn:lri:entity_type:property_type")
                t["urn:lri:property_type:types"] =list(set(t["urn:lri:property_type:types"]))
            t["urn:lri:property_type:supertypes"] = ["urn:lri:entity_type:property"]

        # resolve specific_properties to FQUIDs
        for tid,t in self.index["id"].items():
            if "urn:lri:property_type:specific_properties" in t:
                sps = []
                for sp in t["urn:lri:property_type:specific_properties"]:
                    if sp in self.index["properties"]:
                        sps.append(self.index["properties"][sp])
                    else:
                        sps.append(sp)
                sps.sort()
                t["urn:lri:property_type:specific_properties"]=sps
                

        # Now we can handle our tree of type dependencies
        self.log.debug("RESOLVING DEPENDENCIES....")
        self.log.debug(repr(self.index["id"]))
        success = self.resolve_dependency_tree()
        self.log.debug("DONE")

        if self.errors:
            return False
        
        # Figure out if we have any reverse/primary property contradictions.
        #if in_bootstrap:
        self.log.debug("RESOLVING REVERSE PROPERTIES -- ")
        success = self.resolve_reverse_properties()
        self.log.debug("REVERSE PROPERTY RESOLUTION SUCCESSFUL =",success)
        # self.log.debug(objecttype, json.dumps(t),"\n\n"
        if self.errors:
            self.log.debug(repr(self.errors))
            return False

        return True

 
    def resolve_dependency_tree(self):

        self.type_order=[]
        ancestors={}
        properties={}
        deps={}

        self.log.debug("GET PARENTS")
        # Get immediate parent types (and properties while we're there)
        for tid,t in self.index["id"].items():
            ancestors[tid] = set(t.get("urn:lri:property_type:supertypes",[]))
            properties[tid] = set(t.get("urn:lri:property_type:specific_properties",[]))
            deps[tid]=set()
                
        self.log.debug("ANCESTORS COUNT =",len(ancestors))
        self.log.debug("PROPERTIES COUNT =",len(properties))
        self.log.debug("DEPS COUNT =",len(deps))

        self.log.debug("RESOLVE")
        # Now iterate till there are no more changes
        new_change_count = 0
        first_pass = True
        itercount = 0
        old_change_count = 0
        new_change_count = 0
        while ( new_change_count > 0 or first_pass ):
            if itercount > len(ancestors) * 10:
                self.errors.append("Stuck in dependency resolution loop.")
                break
            itercount += 1
            self.log.debug("NEW CHANGE COUNT =",new_change_count)
            first_pass = False
            for tid,pids in copy.deepcopy(ancestors.items()):
                old_change_count = new_change_count
                new_change_count = 0
                oldpids=copy.copy(pids)
                for pid in pids:
                    g = deps.keys()
                    g.sort()
                    #self.log.debug('ALLDEPS',json.dumps(g,indent=4,sort_keys=True))
                    self.log.debug("DEPENDENCY PARENT ",pid,"CHILD",tid)
                    deps[pid].add(tid)
                    ancestors[tid].update(ancestors[pid])
                    properties[tid].update(properties[pid])
                if oldpids != ancestors[tid]:
                    new_change_count += 1

        self.log.debug("ANCESTORS AND PROPERTIES")
        # Now we can fill in the "ancestors" and "properties" props
        for tid,t in self.index["id"].items():
            if ancestors[tid]:
                t["urn:lri:property_type:ancestors"] = list(ancestors[tid])
                t["urn:lri:property_type:ancestors"].sort()
            if properties[tid]:
                t["urn:lri:property_type:properties"] = list(properties[tid])
                t["urn:lri:property_type:properties"].sort()

        #self.log.debug(repr(self.index["id"]))

        if self.errors:
            return False
        
        self.log.debug("GENERATE......")
        # Generate an ordering of types with no dependencies
        itercount = 0
        while (len(self.type_order) < len(self.index["id"])):
            if itercount > len(self.index["id"]) * 2:
                self.errors.append("Stuck in type dependency ordering loop.")
                break
            itercount += 1
            self.log.debug(len(self.type_order),  len(self.index["id"]))
            for tid,children in deps.items():
                if children:
                    self.log.debug("TID LEN(CHILDREN) IN_TYPE_ORDER",tid,len(children),tid in self.type_order)
                    #self.log.debug("CHILDREN",sorted(list(children)))
                    #self.log.debug("ANCESTORS",sorted(list(ancestors[tid])))
                if not children and tid not in self.type_order:
                    self.type_order.append(tid)
                    for aid in ancestors[tid]:
                        # Because tid is now in the order list, we can remove it as a dependency
                        if tid in deps[aid]:
                            deps[aid].remove(tid)
                else:
                    # Failsafe to break loops
                    if tid in deps[tid]:
                        self.log.debug("TYPE DEPENDENCY LOOP FOR TYPE:",tid,deps[tid])
                        if self.in_test_mode:
                            self.errors.append("TYPE DEPENDENCY LOOP FOR TYPE:"+repr(tid)+" : "+repr(deps[tid]))
                            return False
                        else:
                            deps[tid].remove(tid)

        if self.errors:
            return False
        self.log.debug("DONE")
        self.type_order.reverse()
        
        return True
               

    def resolve_reverse_properties(self):
        
        primary={}
        reverse={}
        pids = self.index['properties'].values()

        self.log.debug(self.index['properties'])
        # First lets extract our pid pairs
        for pid in pids:
            pt = self.index['id'][pid]
            self.log.debug("PROPERTT TYPE OBJECT",pt)
            revpid = pt.get('urn:lri:property_type:reverse')
            self.log.debug("IS PRIMARY",pt["urn:lri:property_type:id"],pt["urn:lri:property_type:is_primary"])
            if revpid:
                if pt['urn:lri:property_type:is_primary'] == True:
                    primary[pid] = revpid 
                else:
                    reverse[pid] = revpid
            
        self.log.debug("INITIAL PRIMARY",primary)
        self.log.debug("INITIAL REVERSE",reverse)
    
        # Make sure we don't have dupes
        target={}
        for pid in pids:
            pt = self.index['id'][pid]
            revpid = pt.get('urn:lri:property_type:reverse')
            if revpid:
                self.log.debug("REVERSE OF",pid,"IS CLAIMED TO BE",revpid)
                if revpid not in target:
                    target[revpid]=[]
                target[revpid].append(pid)
        
        for revpid,pidlist in target.items():
            if len(pidlist) > 1:
                self.errors.append("Multiple property types %s have reverse pointing to %s" % (str(pidlist),revpid))
        if self.errors:
            return False

        # Now let's make sure loops are consistent.
        for pid in pids:
            if pid in primary and primary[pid] in reverse:
                if reverse[primary[pid]] != pid:
                    self.errors.append("Open reverse property loop %s --> %s --> %s" % (pid,primary[pid],reverse[primary[pid]]))
            #self.log.debug("CONSISTENCY:",pid,pid in primary,self.index['id'][pid].get('reverse'),self.index['id'][pid].get('reverse') in primary)
            if pid in primary and self.index['id'][pid].get('urn:lri:property_type:reverse') in primary:
                self.errors.append("Two primary properties in loop %s <--> %s" % (pid,self.index['id'][pid].get('urn:lri:property_type:reverse')))
            if pid in reverse and self.index['id'][pid].get('urn:lri:property_type:reverse') in reverse:
                self.errors.append("Two reverse properties in loop %s <--> %s" % (pid,self.index['id'][pid].get('urn:lri:property_type:reverse')))
        if self.errors:
            return False

        # Now we complete partial loops
        for pid in pids:
            if pid in primary and primary[pid] not in reverse:
                self.index['id'][primary[pid]]['urn:lri:property_type:reverse'] = pid
            elif pid in reverse and reverse[pid] not in primary:
                self.index['id'][reverse[pid]]['urn:lri:property_type:reverse'] = pid

        # Make sure reverse properties point to primary
        for pid in reverse:
            if not self.index['id'][pid].get('urn:lri:property_type:reverse'):
                self.errors.append("Reverse property %s missing reference to primary" %(pid))
        if self.errors:
            return False

        self.log.debug("PRIMARY",primary)
        self.log.debug("REVERSE",reverse)
        primary={}
        reverse={}
        # First lets extract our pid pairs
        for pid in pids:
            pt = self.index['id'][pid]
            revpid = pt.get('urn:lri:property_type:reverse')
            if revpid:
                if pt['urn:lri:property_type:is_primary'] == True:
                    primary[pid] = revpid
                else:
                    reverse[pid] = revpid

        #self.log.debug("PIDS",pids)
        self.log.debug("FINAL PRIMARY",primary)
        self.log.debug("FINAL REVERSE",reverse)


        return True


                   

    def push_bootstrap_to_db(self,db):

        for tid in self.type_order:
            self.log.debug("Inserting type:",tid)
            self.log.debug(repr(self.index["id"][tid]))
            e=entity.entity(rec=self.index["id"][tid],db=db,creator=db.creator_guid)
            if e.errors:
                self.log.debug("ERROR PUSHING TO DB IN INIT",e.errors,self.index["id"][tid])
                raise Exception
            else:
                e.create()
            if e.errors:
                self.log.debug("ERROR PUSHING TO DB IN CREATE",e.errors,self.index["id"][tid])



    def load_from_neodb(self,db):

        schema_objects=[]
        old = 0
        r = db.entity_search({"urn:lri:property_type:types":"urn:lri:entity_type:type",
                              "limit":100000},
                              include_details=True,
                              in_bootstrap=True)
        schema_objects.extend(r['entities'])
        self.log.debug("NUMBER OF OBJECT TYPES =",len(schema_objects))
        old = len(schema_objects)
        r = db.entity_search({"urn:lri:property_type:types":"urn:lri:entity_type:datatype",
                              "limit":100000},
                              include_details=True,
                              in_bootstrap=True)
        schema_objects.extend(r['entities'])
        self.log.debug("NUMBER OF DATA TYPES =",len(schema_objects) - old)
        old = len(schema_objects)
        r = db.entity_search({"urn:lri:property_type:types":"urn:lri:entity_type:property_type",
                              "limit":100000},
                              include_details=True,
                              in_bootstrap=True)
        self.log.debug(r)
        schema_objects.extend(r['entities'])
        self.log.debug("NUMBER OF PROPERTY TYPES =",len(schema_objects) - old)
        
        #for so in schema_objects:
        self.log.debug("SCHEMA OBJECTS:",repr(schema_objects),":")
        self.s = self.digest_search_response(schema_objects,db=db)

        self.process_loaded_schema(in_bootstrap=False,db=db)

        
    def digest_search_response(self,r,db=None):

        s = { "datatypes": {},
              "types": {},
              "properties": {} }
    
        for e in r:
            rec={}
            for pid,pdict in e["props"].items():
                pid = db.get_best_id(pid,in_bootstrap=True)
                pid=re.sub(".+:","",pid) 
                rec[pid]=[]
                for value in pdict.keys():
                    if "guid" not in pid:
                        value = db.get_best_id(value,in_bootstrap=True)
                    rec[pid].append(value)
                if pid == "id":
                    tid = rec["id"][0]
                    self.log.debug("PROCESSED:",tid)
                    if ':entity_type:' in tid:
                        etype = "types"  # Is object type
                    elif ':data_type:' in tid:
                        etype = "datatypes"  # Is object type
                    elif ':property_type:' in tid:
                        etype = "properties"  # Is object type
                    else:
                        etype = None
                        self.log.debug("BAD ETYPE FOR ",pdict,rec)
                if len(rec[pid]) == 1 and pid not in ["urn:lri:property_type:types","urn:lri:property_type:supertypes","urn:lri:property_type:ranges","urn:lri:property_type:properties","urn:lri:property_type:specific_properies","urn:lri:property_type:ancestors","urn:lri:property_type:subtypes","urn:lri:property_type:domains"]:
                    rec[pid]=rec[pid][0] # No need for lists of length 1

            # Index GUID --> URI ID for lookup later
            self.index["guid"][rec["guid"]] = rec["id"]
                
            if etype:        
                s[etype][tid]=rec
                self.log.debug("DIGESTED",etype,tid,rec,pdict)
            else:
                self.errors.append("BAD SCHEMA OBJECT:")
                self.errors.extend(json.dumps(rec,indent=4,sort_keys=True).split("\n"))
                self.log.debug("BAD OBJECT TYPE!!!!\n\n")
                self.log.debug(repr(rec))
            self.log.debug("IN DIGEST",s.keys(),etype)
            self.log.debug("S SIZE",etype,len(s[etype]))
                
        return s

        #for h in hits:
        #    self.s[h["id"]]=
            

    def is_valid_property(self,proptype):

        if proptype not in self.index['id']:
            self.log.debug("INVALID PROPERTY:",proptype)
            self.log.debug("ALL TYPES",len(self.index['id']),repr(sorted(self.index['id'].keys())))
            self.log.debug("ALL PROP TYPES",len(self.index['properties']),repr(sorted(self.index['properties'].keys())))
            return False
        return True

    def primary_proptype(self,proptype):
        ''' Get primary proptype if we are a reverse proptype '''

        # Make sure we can get the property
        if proptype not in self.index['id']:
            proptype=self.index["guid"].get(proptype)
        if proptype not in self.index['id']:
            return False
        
        if self.index['id'][proptype]['urn:lri:property_type:is_primary'] == True:
            # We are primary, so we return ourselves
            return proptype
        else:
            self.log.debug("NON-PRIMARY",proptype,self.index['id'][proptype])
            return self.index['id'][proptype]['urn:lri:property_type:reverse']

    def reverse_proptype(self,proptype):
        ''' Get reverse proptype if we are a primary proptype '''

        if proptype not in self.index['id']:
            proptype=self.index["guid"].get(proptype)
        if proptype not in self.index['id']:
            return False

        if self.index['id'][proptype]['urn:lri:property_type:is_primary'] != True:
            # We are primary, so we return ourselves
            return proptype
        else:
            #self.log.debug("NON-REVERSE",proptype,self.index['id'][proptype])
            return self.index['id'][proptype].get('urn:lri:property_type:reverse','')
            
    def is_bootstrap_primary(self,proptype):
        ptfields=proptype.split(":")
        if ptfields[-1] in primaries:
            return True
        else:
            return False

    def property_target_kind(self,proptype,in_bootstrap=False):
        if in_bootstrap:
            ptfields=proptype.split(":")
            if ptfields[-1] in literals:
                return "literal"
            else:
                return "link"

        if proptype not in self.index['id']:
            return None

        ranges = self.index['id'][proptype]["urn:lri:property_type:ranges"]
        if isinstance(ranges,list):
            ranges=ranges[0]
        if ":data_type:" in ranges:
            #self.log.debug("TARGET PROPKIND LITERAL",proptype,ranges)
            return "literal"
        elif ":entity_type:" in ranges:
            #self.log.debug("TARGET PROPKIND LINK",proptype,ranges)
            return "link"
        else:
            self.log.debug("TARGET PROPKIND UNKNOWN",proptype,ranges)
            self.errors.append("Unknown property kind for property ID: "+repr(proptype))
            return None

    def save_to_archive(self,prefix):
        fh = open(prefix+".lri_schema_archive.json","w")
        fh.write(json.dumps({"s":self.s,"index":self.index,"creator":self.creator},sort_keys=True,indent=4))
        fh.close()

    def load_from_archive(self,prefix):
        fh = open(prefix+".lri_schema_archive.json")
        data = json.loads(fh.read())
        fh.close()
        self.s = data['s']
        self.index = data['index']
        self.creator = data['creator']
 
def test():
    s=schema()
    s.load_bootstrap_file()
    
            
    
if __name__=="__main__":
    test()
