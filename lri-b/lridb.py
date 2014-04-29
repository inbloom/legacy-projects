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

import json,schema,random,hashlib,datetime,copy,prop,timer,zlib,base64,traceback,lrilog


default_creator_guid = "LRI_DEFAULT_CREATOR_GUID"

wildcard_allowed_properties = ["urn:lri:property_type:name","urn:lri:property_type:label"]

immutable_props=["urn:lri:property_type:guid",
                 "urn:lri:property_type:timestamp",
                 "urn:lri:property_type:creator"]

def random_guid():
    return hashlib.md5(str(random.random())).hexdigest()

def make_cursor(s):
    if s == False:
        return False
    return(base64.urlsafe_b64encode(zlib.compress(json.dumps(s))))


def parse_cursor(s):
    return(json.loads(zlib.decompress(base64.urlsafe_b64decode(s.encode('utf-8')))))



class lridb(object):

    def __init__(self,config=None,configfilename="./lri_config.json",create_indices=False,in_test_mode=False,verbose=False):
        self.configfilename = configfilename
        if config:
            self.config = config
        else:
            self.config = json.loads(open(self.configfilename).read())
        self.dbdir=self.config.get('neo4j_dir',"./db")
        self.log = lrilog.lrilog("LRIDB",verbose=verbose,outfilename=self.dbdir+"/LRI_DEBUG.log")
        self.server_url = "http://%s:%d/db/data/" % (self.config.get('neo4j_server_host','localhost'),
                                                     self.config.get('neo4j_server_port',7474))
        self.bootstrap_filenames = self.config.get('bootstrap_filenames',[])
        self.creator_guid=self.config.get('default_creator_guid',default_creator_guid)
        self.in_test_mode = in_test_mode
        if create_indices or in_test_mode:
            self.in_bootstrap = True
        else:
            self.in_bootstrap = False
        self.link_index=None
        self.attr_index=None
        self.errors=[]
        self.warns=[]

        # Boot up
        if not self.in_test_mode:
            self.open()
        self.boot(create_indices=create_indices)

    def create_property(self,origrec,node=None,in_bootstrap=False,is_update=False):

        rec = copy.deepcopy(origrec)
        self.log.debug("CREATE PROPERTY:",json.dumps(rec))
        ''' Create a property on an existing node. Nodes referred by ID must be unique '''

        proptype = rec.get("proptype")

        if not in_bootstrap:
            if not self.schema.is_valid_property(proptype) or proptype not in self.schema.index['id']:
                self.errors.append("Cannot create property with invalid proptype = %s" % (proptype))
                return False

        creator = rec.get("creator",self.creator_guid)

        if "value" not in rec and not rec.get("to"):
            self.errors.append("Cannot create property with missing or null value/target.")
            return False

        propkind = self.schema.property_target_kind(proptype,in_bootstrap=self.in_bootstrap)
        from_guid = rec["from"] 
        to_guid = None

        # Find our node
        if not node:
            # Find our node
            node = self.get_entity(from_guid)
        if not node:
            self.errors.append("Property create failure. Node not found with id = "+repr(from_guid))
            return False

        # Check to see if our property already exists
        # Along the way determine if our property is "complete"

        # Unique property?
        if not is_update and self.schema.index['id'][proptype]["urn:lri:property_type:is_unique"] == True:
            unique_existing = self.property_search({"from":from_guid,
                                                    "proptype":proptype,
                                                    "alive":True,
                                                    "creator":creator})
            if self.errors:
                return False

            #  If this is not a delete and prop already exists, we skip creation
            if unique_existing and rec.get("alive",True):
                self.log.debug("UNIQUE PROPERTY ALREADY EXISTS.  SKIPPING CREATION OF DUPLICATE")
                return unique_existing[0]["internal"]  # Ignoring the disaster of there being more than one hit


        if propkind == "literal":
            if "value" not in rec:
                self.errors.append("Literal property creation failure. Missing value")
                return False
            existing = self.property_search({"from":from_guid,
                                             "proptype":proptype,
                                             "value":rec["value"],
                                             "alive":rec.get("alive",True),
                                             "creator":creator})
            if self.errors:
                return False
            
            rec["complete"] = True
            target_node = self.null_node
        
            # Make sure this ID has not already been used
            if not existing and rec['proptype'] == 'urn:lri:property_type:id':
                plist = self.property_search({"value":rec["value"],
                                              "proptype":"urn:lri:property_type:id",
                                              "complete":True})
                if plist:
                    self.errors.append("Entity %s already has ID %s. Cannot be assigned to %s" %(plist[0].get("from",""),rec["value"],from_guid))
                    return False

        elif propkind == "link":
            if rec.get("to"):
                to_guid = rec["to"]
                target_node = self.get_entity(to_guid)
                if target_node:
                    existing = self.property_search({"from":from_guid,
                                                     "proptype":proptype,
                                                     "to":to_guid, 
                                                     "creator":creator})
                    if self.errors:
                        return False
                    rec["complete"] = True
                else:
                    self.errors.append("Property create failure. Target node does not exist for target GUID = "+repr(to_guid))
                    return False
            else:
                # Validate our ID and bail if we can't
                #id_errors = self.problems_with_id(rec["value"])
                #if id_errors:
                #    self.errors.extend(id_errors)
                #    self.log.debug("\n\n\n\n\nFAILED TO VALIDATE ID %s \n\n\n\n" % (rec["value"])
                #    return False

                to_guids = self.get_guids(rec["value"])
                if to_guids:
                    to_guid = to_guids[0] # Choose first GUID
                    rec["to"] = to_guid
                    target_node = self.get_entity(to_guid)

                    if not target_node:
                        self.errors.append("Property create failure. Target node does not exist for target GUID = "+repr(to_guid))
                        return False  # It should be impossible to get here.

                    del rec["value"]  # Don't need value since we resolved to target GUID
                    existing = self.property_search({"from":from_guid,
                                                     "proptype":proptype,
                                                     "to":to_guid, 
                                                     "creator":creator})
                    if self.errors:
                        return False
                    rec["complete"] = True
                else:
                    # We have a link to an entity that does not yet exist
                    existing = self.property_search({"from":from_guid,
                                                     "proptype":proptype,
                                                     "value":rec["value"],
                                                     "creator":creator})
                    if self.errors:
                        return False
                    rec["complete"] = False
                    target_node = self.null_node
        else:
            self.errors.append("Illegal property kind %s" % (repr(propkind)))
            return False

        if existing and rec.get("alive",True):
            self.log.debug("PROPERTY ALREADY EXISTS.  SKIPPING CREATION OF DUPLICATE")
            return existing[0]["internal"]  # Ignoring the disaster of there being more than one hit
        
        # Our property does not yet exist, so we can create it.
        self.log.debug("PROPERTY DOES NOT YET EXIST =",rec)


        failure = False

        # Set our default administrative values
        rec["replaced_by"]=""
        rec["alive"]=origrec.get("alive",True) # Would only be False when property creation is actually a property deletion
        rec["guid"] = random_guid()
        rec["timestamp"] = datetime.datetime.utcnow().isoformat()
        rec["creator"] = creator
        if self.null_node != target_node:
            rec["to"] = target_node["guid"]


        # Reverse this property if we need to
        proptype = rec["proptype"]
        if not self.schema.is_valid_property(proptype):
            self.errors.append("Proptype %s does not exist" % (proptype))
            #raise Exception
            return False

        primary_proptype = self.schema.primary_proptype(proptype)

        if primary_proptype != proptype:
            # We are a reverse property, so swap our constraints
            f = rec.get("from")
            t = rec.get("to")
            if f:
                del rec["from"]
            if t:
                del rec["to"]
            if f:
                rec["to"] = f
            if t:
                rec["from"] = t
        rec['proptype'] = primary_proptype

        link = self.write_and_index_property(node,rec,primary_proptype,target_node)

        # If we are adding an id to an entity, look for 
        # incomplete link properties that point to this entity
        # and complete the "from" or "to" from a lookup on the "value"
        if rec['proptype'] == 'urn:lri:property_type:id':
            plist = self.property_search({"value":rec["value"],
                                           "complete":False})
            for prec in plist:
                self.complete_property(prec,from_guid)


        if failure:
            return False
        else:
            return link


    def get_guids(self,eid,in_bootstrap=False):
        precs = self.property_search({"value":eid,
                                      "proptype":"urn:lri:property_type:id"},
                                      in_bootstrap=in_bootstrap)

        return (sorted([p["from"] for p in precs]))



    def parse_search_constraints(self,constraints,in_bootstrap=False):

        q = {'subqueries':[], 'starts':[], 'leftover_results':[]}

        c = None
        for k,v in constraints.items():

            #if isinstance(v,list):
            #    v = set(v) # dedupe
            #    constraint_expr = '('+(' OR '.join(['"'+term+'"' for term in v]))+')'
            #else:
            #    constraint_expr = v 
            constraint_expr = v
            
            if k == 'cursor':
                try:
                    q['cursor'] = v
                    if v:
                        c = parse_cursor(v)
                except Exception, e:
                    self.errors.append("Invalid cursor: %s" %(repr(v)) + ":"+ traceback.format_exc())
                    return None
            elif k == 'creator':
                q['creator'] = v
            elif k == 'as_of':
                q['as_of'] = v
            elif k == 'shape':
                q['shape'] = v
            elif k == 'constrain_by':
                q['constrain_by'] = v
            elif k == 'alive':
                q['alive'] = v
            elif k == 'limit':
                try:
                    q['limit'] = int(v)
                except:
                    self.errors.append("Invalid integer for 'limit' parameter %s" % (repr (v)) + ":"+ traceback.format_exc())
                    return None
            else:
                if len(k) > 1 and k[1] == '~':
                    # We've got a prefix for logical AND with the same proptype
                    k = k[2:]
                propkind = self.schema.property_target_kind(k,in_bootstrap=in_bootstrap)
                if not propkind:
                    self.errors.append("Invalid property type: %s" %(repr(k)) )
                    return None 
                q['starts'].append(0)
                self.log.debug("ENTITY SEARCH PROPKIND",constraint_expr, propkind)
                if propkind == 'link':
                    guids = self.get_guids(v,in_bootstrap=in_bootstrap) # only works for single GUID value
                    if guids:
                        q['subqueries'].append({'proptype':k,'to':guids[0]})  # No worrying about dupes
                    else:
                        q['subqueries'].append({'proptype':k,'value':v})
                else:
                    q['subqueries'].append({'proptype':k,'value':v})

        # Use cursor data if we have it
        if c:
            # If we have a cursor, we are not allowed to also specify the query.
            for f in ['creator','as_of','shape','subqueries']:
                if f in q:
                    del q[f]
                    q['subqueries'] = c['subqueries']  #NOTE:  These are 'resolved' subqueries.
            q.update(c)

        # Default limit
        if 'limit' not in q:
            q['limit'] = 25

        return q


    def perform_subqueries(self,q,results,creator=None,in_bootstrap=False):

        self.log.debug("ALL SUBQUERIES:",q['subqueries'])
        for i in range(len(q['subqueries'])):
            sq = copy.deepcopy(q['subqueries'][i])
            if creator:
                sq['creator'] = creator
            self.log.debug("ATTEMPTING SUBQUERY:",sq)
            hit_guids = self.property_constraint_search(sq,
                                                        limit=q['limit'],
                                                        start=q['starts'][i],  # GUESS: sq limit should be same as for q
                                                        in_bootstrap=in_bootstrap)

            q['starts'][i] += len(hit_guids)

            if i == 0:
                # First hit, so get everything
                self.log.debug("FIRST SEARCH RESULTS",hit_guids)
                results = hit_guids
            else:
                # Intersect with previous hits
                self.log.debug("INTERSECT WITH",hit_guids)
                results &= hit_guids  # Intersect the result sets
                self.log.debug("INTERSECTION",results)


        #  Now do shape constraints if we have them
        if 'constrain_by' in q:
            constrained_results = []
            for guid in results:
                if self.constrain_by_shape(guid,q['constrain_by']):
                    self.log.debug("SHAPE CONSTRAINT MET:",guid)
                    constrained_results.append(guid)
                else:
                    self.log.debug("SHAPE CONSTRAINT NOT MET:",guid)
                
        else:
            self.log.debug("NO SHAPE CONSTRAINT:",q)
            constrained_results = results

        return constrained_results

        
    def entity_search(self,constraints,include_internal_objects=True,
                      include_details=True,in_bootstrap=False,get_history=False):


        q = self.parse_search_constraints(constraints,in_bootstrap)

        if not q:
            return {"cursor":None,"entities":[]}
        
        self.log.debug("RESOLVED QUERY",q,self.errors)
        # Assemble our subqueries
        '''
        for i in range(len(q['subqueries'])):

            for f in ['creator']:
                if q['subqueries'][i].get(f):
                    sq[f] = q['subqueries'][i][f]
            
                # Need to deal with as_of later XXXXX
                #if as_of:
                #sq['timestamp'] = '{0 TO %s}]' % v # Lucene range query for strings
        '''
        # Run our subqueries
        old_results = set((q['leftover_results']))
        new_results = set()

        # Max tries is the number of iterations we attempt get get enough results
        # If we run out of tries, it probably means the query is taking too long
        # (e.g. We are intersecting large sets with little overlap)
        max_tries = 10
        try_count = 0

        while len(old_results | new_results) < q['limit'] and try_count < max_tries:
            new_results = set(self.perform_subqueries(q,new_results,creator=q.get('creator'),in_bootstrap=in_bootstrap))
            try_count += 1
            if len(new_results) > 0 and len(new_results) < q['limit']:
                # We've run out of results
                break
        self.log.debug("COMPLETED QUERIES:",json.dumps(q['subqueries'],indent=4,sort_keys=True))

        final_results = list(old_results | new_results)
        #self.log.debug("FINAL RESULTS",q['limit'],old_results,new_results)

        result_page = final_results[:q['limit']]
        self.log.debug("RESULT PAGE",result_page)
        if len(final_results)> q['limit']:
            # Save our extras for the next page
            q['leftover_results'] = final_results[q['limit']:]
            new_cursor = True
        else:
            # We finished the last page
            new_cursor = False

        if new_cursor:
            # Assemble our new cursor
            new_cursor = {'subqueries':q['subqueries'],
                          'starts':q['starts'],
                          'leftover_results':q['leftover_results']}

            for f in ['creator','as_of','shape']:
                if f in q:
                    new_cursor[f] = q[f]
                
        #  Now we can get our entities
        entities = []
        for guid in result_page:
            entities.append(self.get_entity_properties(guid,
                                                       include_internal_objects=include_internal_objects,
                                                       include_details=include_details,
                                                       proplimit=100,
                                                       creator=q.get('creator'),
                                                       shape=q.get('shape'),
                                                       alive=q.get('alive',True),
                                                       get_history=get_history,
                                                       in_bootstrap=in_bootstrap))
        self.log.debug("CURSOR",new_cursor)
        return ({"cursor":make_cursor(new_cursor),"entities":entities})

                
        
    #@timer.timer("property_constraint_search")
    def property_constraint_search(self,constraints,
                                   limit=25,
                                   start=0,
                                   include_details=False,
                                   include_internal_objects=False,
                                   in_bootstrap=False):



        # Arrays of target values/IDs and creators are considered to be OR'ed together
        scs = []
        if 'to' in constraints:

            if 'value' in constraints:
                del constraints['value']

            if not isinstance(constraints.get('to'),list):
                tos = [constraints['to']]
            else:
                tos =  constraints['to']
            sc = copy.deepcopy(constraints)
            for t in tos:
                sc['to'] = t
                scs.append(copy.deepcopy(sc))

        elif 'value' in constraints:
            if not isinstance(constraints.get('value'),list):
                values = [constraints['value']]
            else:
                values =  constraints['value']
            sc = copy.deepcopy(constraints)
            for v in values:
                sc['value'] = v
                scs.append(copy.deepcopy(sc))
        else:
            # Not constraining by value or to
            scs.append(copy.deepcopy(constraints))
                
        if 'creator' in constraints:
            if not isinstance(constraints.get('creator'),list):
                creators = [constraints['creator']]
            else:
                creators = constraints['creator']

            final_scs = []
            for c in creators:
                fcs = copy.deepcopy(scs)
                for sc in fcs:
                    sc['creator'] = c
                    final_scs.append(copy.deepcopy(sc))
        else:
            final_scs = scs

        self.log.debug("ALL SUBCONSTRAINTS:",final_scs)

        # Now we have many queries and will union the results

        # if the number of queries to perform is too large, then let's
        # consider this to be an error

        if len(final_scs) > 100:
            self.errors.append("Use of logical OR is too aggressive.  Query would be very slow.  Try breaking query into pieces using less OR.")
            return []
        
        hits = []
        for cs in final_scs:
            sh = self.property_search(constraints=cs,in_bootstrap=in_bootstrap,start=start)
            if sh == False:
                self.log.debug(self.errors)
                return None
            else:
                self.log.debug("SUBCONSTRAINTS:",cs)
                self.log.debug("SUBHITS:",repr(sh))
                hits.extend(sh)
        self.log.debug("CONSTRAINTS:",constraints)
        self.log.debug("HITS:",repr(hits))
        node_guids = set([h["from"] for h in hits])

        return node_guids

    def get_entity_properties(self,guid,
                              include_internal_objects=True,
                              include_details=True,
                              proplimit=100,
                              shape=None,
                              creator=None,
                              get_history=False,
                              alive=True,
                              in_bootstrap=False):

        n = self.get_entity(guid)

        #prop_links = self.link_index.query["from"][guid]
        #e = copy.deepcopy(self.internal_properties(n))  # Get immediate neo4j properties
        e={}
        if include_internal_objects:
            e["internal"] = n
        e["props"] = {}

        # Get our property values
        #self.log.debug("ENTITY GUID",e["guid"])
        #timer.start("rel_crawl")
        for r in self.links_of_node_gen(n):

            p = json.loads(r["rec"])

            # Filter by creator
            if creator and p['creator'] != creator:
                continue

            if p['alive'] != alive:
                continue

            if not get_history and p["replaced_by"] != "":
                continue

            if include_internal_objects:
                p["internal"] = r

            # We have to consider the direction of the link when presenting properties
            if in_bootstrap:
                propkind = self.schema.property_target_kind(p["proptype"],in_bootstrap=in_bootstrap)
                if propkind == 'literal':
                    primary_proptype = p["proptype"]
                else:
                    if guid == p.get("from") or self.schema.is_bootstrap_primary(p["proptype"]):
                        primary_proptype = p["proptype"]
                        reverse_proptype = "UNKNOWN"
                    else:
                        primary_proptype = 'UNKNOWN'
                        reverse_proptype = p["proptype"]
                        #self.log.debug(self.schema.index['id'].keys())
                        #primary_proptype = self.schema.primary_proptype(p["proptype"])
                        #raise Exception
            else:
                primary_proptype = self.schema.primary_proptype(p["proptype"])
                if primary_proptype != p["proptype"]:
                    reverse_proptype = p["proptype"]
                else:
                    reverse_proptype = self.schema.reverse_proptype(p["proptype"])

            if guid == p.get("from"):
                direction = "forward"
                visible_proptype = primary_proptype
            elif guid == p.get("to"):
                direction = "backward"
                visible_proptype = reverse_proptype
            else:
                self.log.debug("YIKES!")
                raise Exception

            #self.log.debug("DIRECTION",direction,visible_proptype)
            if visible_proptype in ['UNKNOWN','']:
                continue  # We can't see this property

            #timer.start("extract")
            if include_details:
                # We want detailed property records
                if visible_proptype not in e["props"]:
                    e["props"][visible_proptype]={}
                if "value" in p:
                    if p["value"] not in e["props"][visible_proptype]:
                        e["props"][visible_proptype][p["value"]] = []
                    e["props"][visible_proptype][p["value"]].append(p)
                else:
                    self.log.debug("ADDING PROPERTY DETAIL:",p)
                    if direction == "forward":
                        if p["to"] not in e["props"][visible_proptype]:
                            e["props"][visible_proptype][self.get_best_id(p["to"],in_bootstrap=True)] = []
                        e["props"][visible_proptype][self.get_best_id(p["to"],in_bootstrap=True)].append(p)
                    else:
                        if p["from"] not in e["props"][visible_proptype]:
                            e["props"][visible_proptype][self.get_best_id(p["from"],in_bootstrap=True)] = []
                        e["props"][visible_proptype][self.get_best_id(p["from"],in_bootstrap=True)].append(p)
            else:

                # We only a simple list of values
                if visible_proptype not in e["props"]:
                    e["props"][visible_proptype]=set()
                if "value" in p:
                    if p["value"] not in e["props"][visible_proptype]:
                        e["props"][visible_proptype].add(p["value"])
                else:
                    if direction == "forward":
                        if p["to"] not in e["props"][primary_proptype]:
                            e["props"][visible_proptype].add(self.get_best_id(p["to"]))
                    else:
                        if p["from"] not in e["props"][reverse_proptype]:
                            e["props"][visible_proptype].add(self.get_best_id(p["from"]))
            #timer.end("extract")
        #timer.end("rel_crawl")
        if not include_details:
            for proptype in e["props"]:
                e["props"][proptype] = list(e["props"][proptype])
                if len(e["props"][proptype]) > 1:
                    e["props"][proptype].sort() # Sort natively
                else: 
                    # Only one value in list. Replace the list with the value
                    e["props"][proptype]=e["props"][proptype][0]
        # Sort by rank if it exists
        #e["props"][p["proptype"]].sort(lambda a,b: cmp(a.get("rank",0),b.get("rank",0)))

        # If we requested a shape, get it
        #self.log.debug("E ",e)
        if shape and e.get('props'):
            if not isinstance(shape,dict):
                self.errors.append("Leaves of shape must be subshapes or 'null'")
            else:
                rs = self.get_shape(e,shape,include_details=include_details,get_history=get_history)
                self.log.debug("GOTTEN SHAPE",shape,rs)
                for proptype in shape:
                    e['props'][proptype]=rs[proptype]

        return e
            
    def property_search(self,constraints,in_bootstrap=False,start=None):

        constraints = copy.deepcopy(constraints)
        is_reverse = False

        # Let swap from/to constraints if we are asking for a reverse property
        if 'proptype' in constraints:
            orig_proptype = constraints['proptype']
            value = constraints.get("value","")

            if not in_bootstrap:
                if not self.schema.is_valid_property(orig_proptype):
                    self.warns.append("Proptype %s does not exist" % (orig_proptype))
                    self.log.debug(self.warns,len(self.schema.index['id']))
                    self.log.debug(sorted(self.schema.index['id'].keys()))
                    self.errors.append("Property type '%s' is not valid." % (orig_proptype))
                    #raise Exception
                    return []

                primary_proptype = self.schema.primary_proptype(orig_proptype)
            else:
                primary_proptype = orig_proptype

            constraints['proptype'] = primary_proptype

            # Resolve ID of target into a GUID for link property

            self.log.debug("ORIGINAL_PROPTYPE",orig_proptype)
            self.log.debug("PRIMARY_PROPTYPE",primary_proptype)
            propkind = self.schema.property_target_kind(primary_proptype,in_bootstrap=in_bootstrap)
            self.log.debug("PROPKIND",primary_proptype,propkind)
            if not propkind:
                self.errors.append("BAD PROPTYPE FOR PROP WITH ID: "+repr(primary_proptype))
                self.log.debug(self.errors,self.schema.errors)
                self.log.debug("VALID PROPTYPES\n",sorted(self.schema.index["id"].keys()))
                return []

            if propkind == "link":
                if not constraints.get("to"):
                    if not value.startswith("urn:"):
                        # We were given a GUID rather than an ID
                        target_guid = value
                    else:
                        tguids =  self.get_guids(value,in_bootstrap=in_bootstrap)
                        if tguids:
                            constraints["to"]=tguids[0]  # Ignoring beyond the first
                            if value:
                                del constraints["value"]
                        else:
                            # No hits because the target does not exist
                            return []
            else:
               # Must be literal property
               if 'to' in constraints:
                   del constraints['to']  # Can't have both 'value' and 'to'
 
            # Swap to primary direction if we need to.
            if primary_proptype != orig_proptype:
                is_reverse = True
                # We are a reverse property, so swap our constraints
                f = constraints.get("from")
                t = constraints.get("to")
                if f:
                    del constraints["from"]
                if t:
                    del constraints["to"]
                if f:
                    constraints["to"] = f
                if t:
                    constraints["from"] = t

            


        # By default, let's only get non-deleted latest versions of links
        if "alive" not in constraints:
             constraints["alive"]=True
        #elif constraints["alive"] == None:
        #    del constraints["alive"]
        if "replaced_by" not in constraints:
            constraints["replaced_by"]=""

        props = []
        hits = self.link_search(constraints,start=start)
        #hits = self.link_index.query(q)
        self.log.debug("PROP SEARCH HIT COUNT =",len(hits))

        for l in hits:
            rec = copy.deepcopy(self.internal_properties(l))
            #rec = dict([(k,v) for k,v in l.items()])
            #self.log.debug("PROP HIT:",rec)
            rec["internal"]=l

            # Swap answer back to reverse direction if we are a reverse property
            if is_reverse:
                rec['proptype'] = orig_proptype
                f = rec.get("from")
                t = rec.get("to")
                if f:
                    del rec["from"]
                if t:
                    del rec["to"]
                if f:
                    rec["to"] = f
                if t:
                    rec["from"] = t


            props.append(rec)
            
        return props

    def constrain_by_shape(self,entity_guid,shape):

        overall_match = True
        for proptype,subshape in shape.items():
            plist = self.property_search({"from":entity_guid,
                                          "proptype":proptype})
                
            self.log.debug("IN CONSTRAIN BY SHAPE",proptype,subshape,plist)
            if self.schema.primary_proptype(proptype) == proptype:
                direction = 'forward'
            else:
                direction = 'backward'

            #  This is a constraint match, not a retrieval
            if not isinstance(subshape,dict):
                match = False
                for prec in plist:
                    self.log.debug("CONSTRAIN PREC",prec)
                    if direction == "forward" and 'to' not in prec:
                        self.log.debug("CONSTRAIN USING VALUE:", prec.get("value",""))
                        if prec.get("value","") == subshape:
                        # Non-completed property, so we only have the value
                            match = True
                            break
                    else:
                        self.log.debug("CONSTRAIN USING TO:", prec.get("to",""))
                        splist = self.property_search({"from":prec["to"],
                                                      "proptype":"urn:lri:property_type:id"})
                        for sp in splist:
                            if sp["value"] == subshape:
                                match = True
                                break
                        if match:
                            break
                        else:
                            "TO CONSTRAIN MISS",prec["to"],subshape
            elif subshape:
                match = False
                for prec in plist:
                    match = False
                    if 'to' in prec:
                        match = self.constrain_by_shape(prec['to'],subshape)
                        if match:
                            break
                    else:
                        # Must be a literal property, so match failes
                        match = False
                        break
            else:
                match = True  # Empty "null" always matches
            overall_match &= match
            if not overall_match:
                # If any component fails to match, then the whole thing fails.
                return False

        return overall_match


    def get_shape(self,entity_rec,shape,include_details=False,get_history=False):

        res = {}
        for proptype,subshape in shape.items():
            self.log.debug("IN GET SHAPE",proptype,subshape)
            plist = self.property_search({"from":entity_rec.get("props",{}).get("urn:lri:property_type:guid",""),
                                          "proptype":proptype})
                
            #self.log.debug("SHAPE PROP SEARCH",plist)

            if self.schema.primary_proptype(proptype) == proptype:
                direction = 'forward'
            else:
                direction = 'backward'
            elist = []
            for prec in plist:
                self.log.debug("GETTING SHAPE PROP",prec)
                if not prec.get("to"):
                    continue
                self.log.debug("GET SHAPE ID",proptype,self.schema.primary_proptype(proptype),direction,prec.get("from"),prec.get("to"),type(prec.get("to")))
                esing=self.property_constraint_search({"proptype":"urn:lri:property_type:id",
                                                       "from":prec.get("to","")})
                #else:
                #    esing=self.property_constraint_search({"proptype":"urn:lri:property_type:id",
                #                                           "from":prec["from"]},
                #                                          include_details=include_details,
                #                                          include_internal_objects=False)
                if not esing:
                    continue
                elist.append(self.get_entity_properties(list(esing)[0],
                                                        include_internal_objects=False,
                                                        include_details=include_details,
                                                        proplimit=100,
                                                        shape=subshape,
                                                        get_history=get_history,
                                                        in_bootstrap=False))

            self.log.debug("ELIST",elist)
            #for erec in elist:
            #    # Recurse for lower shapes
            #    if subshape and erec.get("props"):
            #        ss = self.get_shape(erec,subshape,include_details=include_details)
            #        self.log.debug("GOTTEN SHAPE",subshape,ss
            #        for pt in subshape:
            #            erec['props'][pt] = ss[pt]
                
            res[proptype] = elist

        return res


    def complete_property(self,rec,guid):
        ''' When an entity is created for which previously created links point, we need to complete those links. '''
    
        self.log.debug("COMPLETE OLD PROP REC:",rec,guid)

        
        #if rec["complete"] == True:  # Ignore this test, because it could be wrong
        #    # Nothing to do
        #    return None
            
        if rec.get("to") and rec.get("from"):
            self.warns.append("When completing a property, one of 'from' or 'to' should be missing.")
            return False

        newrec={"creator":rec["creator"],
                "proptype":rec["proptype"],
                "complete":True}

        if not rec.get("to") and not rec.get("from"):
            self.warns.append("When completing a property, one of 'from' or 'to' must exist")
            return False

        if not rec.get("to"):
            newrec["to"] = guid  
            newrec["from"] = rec["from"]
        else:
            newrec["from"] = guid
            newrec["to"] = rec["to"]

        self.log.debug("COMPLETE NEW PROP REC:",newrec)
        newp = self.update_property(oldrec=rec,newrec=newrec)

        return newp

    def get_best_id(self,guid,in_bootstrap=False):
        bid = self.schema.index["guid"].get(guid)
        if bid:
            return bid
         # Failed.  So look it up.
        r = self.property_search({"from":guid,
                                  "proptype":"urn:lri:property_type:id"},in_bootstrap=in_bootstrap)
        if r:
            bid = r[0].get("value","")
            if bid:
                self.schema.index["guid"][guid] = bid
                return bid
            
        return guid
                

    def problems_with_id(self,i):
        ''' This is still rather weak '''
        if not i:
            return ["ID is empty"]
        if not isinstance(i,basestring):
            return ["ID %s must be a string but is not" % (repr(i)) ]
        if not i.startswith('urn:'):
            return ["ID '%s' must start with 'urn'" % (i) ]
        parts = i.split(":")
        if len(parts) < 3:
            return ["ID '%s' is missing a namespace" % (i) ]
        return []
                    
                    
        
        
                

                

                

        


        

    


