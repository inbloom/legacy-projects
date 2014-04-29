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
import lridb,json,schema,datetime,copy,prop,timer,time,traceback
import py2neo.neo4j,py2neo.cypher

class neorest(lridb.lridb):

    def open(self):
        self.log.debug(self.server_url)
        self.ndb = py2neo.neo4j.GraphDatabaseService(self.server_url)
        self.ndb.get_indexes(py2neo.neo4j.Node)
        self.log.debug("RAW NODE COUNT =",self.ndb.get_node_count())
        self.log.debug("RAW LINK COUNT =",self.ndb.get_relationship_count())

    def close(self):
        pass

    def boot(self,create_indices=False):

        self.schema = schema.schema(bootstrap_filenames = self.bootstrap_filenames,in_test_mode=self.in_test_mode)

        if self.in_test_mode:
            return

        # Create a right hand side for literal properties stored in link
        self.null_node=self.ndb.get_node(0)
        
        # Make sure our indices are set up
        #self.init_indices()
        self.init_indices(create_indices=create_indices)

        # Get our bootstrap schema
        if create_indices:
            self.schema.load_bootstrap()  # First time load
            self.log.debug(self.schema.errors)
        else:
            self.schema.load_from_neodb(self)


    def init_indices(self,create_indices=True):

        self.node_index = self.ndb.get_or_create_index(py2neo.neo4j.Node,"node_index")
        self.link_index = self.ndb.get_or_create_index(py2neo.neo4j.Relationship,"link_index")

    def create_entity(self,creator=None,max_tries=3):
        self.log.debug("CREATE ENTITY")

        if not creator:
            creator=self.creator_guid

        rec={}
        rec["guid"]=lridb.random_guid()
        rec["timestamp"] = datetime.datetime.utcnow().isoformat()
        rec["creator"] = creator

        self.log.debug("CREATE ENTITY VIA REST",rec)
        success = False
        tries = 0
        while not success or tries == max_tries:
            try:
                n = self.ndb.create(rec)[0]
                success = True
            except Exception, e:
                neoerrs = traceback.format_exc().split("\n")
                time.sleep(0.25)
                tries +=1

        if not success:
            self.errors.append("Too many Neo4J BadRequest errors in node creation!")
            self.errors.extend(neoerrs)
            return None

        self.node_index.add("guid",rec["guid"],n)

        return n

    def internal_properties(self,x):
        return x.get_properties()

    def links_of_node_gen(self,n):
        for link in n.get_relationships():
            yield link

    def write_and_index_property_old(self,node,rec,primary_proptype,target_node,max_tries=3):
        # Now create link to hold actual property and add the literal properties

        success = False
        tries = 0

        while not success and tries < max_tries:
            try:
                link = node.create_relationship_to(target_node,primary_proptype,rec)
                success = True
            except  Exception, e:
                tries += 1
                neoerrs = traceback.format_exc().split("\n")
                time.sleep(0.25)
        if not success:
            self.errors.append("Too many Neo4J errors in relationship creation!")
            self.errors.extend(neoerrs)
            return None
                
        link["rec"]=json.dumps(rec)

        self.log.debug("CREATING LINK INDEX ENTRIES")
        # Index links by from, guid, type, and value, and maybe to
        for f in ["from","to","guid","proptype","value","timestamp","creator","alive","replaced_by","complete"]:
            if f in rec:
                if isinstance(rec[f],basestring):
                    self.link_index.add(f,rec[f].lower(),link)
                else:
                    self.link_index.add(f,str(rec[f]).lower(),link)
                self.log.debug("CREATED LINK INDEX ENTRY",f,rec[f])

        return link

    def write_and_index_property(self,node,rec,primary_proptype,target_node,max_tries=3):
        # Now create link to hold actual property and add the literal properties

        success = False
        tries = 0

        while not success and tries < max_tries:
            try:
                link = node.create_relationship_to(target_node,primary_proptype,rec)
                success = True
            except  Exception, e:
                tries += 1
                neoerrs = traceback.format_exc().split("\n")
                time.sleep(0.25)
        if not success:
            self.errors.append("Too many Neo4J errors in relationship creation!")
            self.errors.extend(neoerrs)
            return None
                
        link["rec"]=json.dumps(rec)

        self.log.debug("CREATING LINK INDEX ENTRIES")
        # Index links by from, guid, type, and value, and maybe to
        batch = py2neo.neo4j.WriteBatch(self.ndb)
        for f in ["from","to","guid","proptype","value","timestamp","creator","alive","replaced_by","complete"]:
            if f in rec:
                if isinstance(rec[f],basestring):
                    batch.add_indexed_relationship(self.link_index,f,rec[f].lower(),link)
                else:
                    batch.add_indexed_relationship(self.link_index,f,str(rec[f]).lower(),link)
                self.log.debug("CREATED LINK INDEX ENTRY",f,rec[f])
        batch.submit()

        return link



    def get_entity(self,guid):
        hits = self.node_index.get("guid",guid)
        if hits:
            return hits[0]
        return None

    def get_prop(self,guid):
        self.log.debug("GET PROP BY GUID:",guid)
        hits = self.link_index.get("guid",guid)
        self.log.debug(hits)
        if hits:
            return hits[0]
        return None

    def form_cypher_query(self,constraints,limit,skip):

        # Normalize for non-strings and escape quotes for strings
        clean_constraints = copy.deepcopy(constraints)
        for k,v in clean_constraints.items():
            if isinstance(v,bool) or isinstance(v,int) or isinstance(v,float):
                clean_constraints[k]=str(clean_constraints[k]).lower()
            elif isinstance(v,basestring):
                clean_constraints[k] = v.replace('\\','\\\\').replace('"','\\"').lower()

        wildcard_search=False
        if 'proptype' in clean_constraints and clean_constraints['proptype'] in lridb.wildcard_allowed_properties and 'value' in clean_constraints and "*" in clean_constraints['value']:
            value = clean_constraints['value']
            value = value.replace('\\','\\\\').replace('"','\\"')
            del clean_constraints['value']
            wildcard_search=True
            
        # First make a lucene query
        lq = ' AND '.join([k+':"'+v+'"' for k,v in clean_constraints.items() if isinstance(v,basestring)])
        self.log.debug("PROPERTY SEARCH LUCENE QUERY:",repr(lq))

        # And then a cypher query from that
        lq = lq.replace('\\','\\\\').replace('"','\\"')

        # If we are searching by name and we have no spaces in the
        # name, then let's do a wildcard search
        if wildcard_search:
            where = ' WHERE r.value =~ "(?i)%s"' % (value)
        else:
            where = ""
        #where = ''
        q = 'START r=relationship:link_index("%s") %s RETURN r' % (lq,where)
        #q = 'START r=relationship:link_index("%s") RETURN r' % (lq)
        if skip:
            q += " SKIP %d" % (skip)
        if limit:
            q += " LIMIT %d" % (limit)
        
        return q.encode('utf-8')

    def link_search(self,constraints,limit=None,start=None,max_tries=3):

        # We use cypher simply to support pagination
        q = self.form_cypher_query(constraints,limit,start)

        self.log.debug("LINK SEARCH CYPHER QUERY:",q)

        # We try a few times due to py2neo bug that causes timeouts
        success = False
        tries = 0
        while not success and tries < max_tries:
            try:
                hits, metadata = py2neo.cypher.execute(self.ndb,q)
                success = True
            except Exception, e:
                tries += 1
                neoerrs = traceback.format_exc().split("\n")
                self.log.debug("FAILING CYPHER QUERY =",repr(q),"-- TRYING %d more times."  % (3-tries))
                time.sleep(0.1)

        if not success:
            self.errors.append("Too many Neo4J errors in cypher query execution!")
            self.errors.extend(neoerrs)
            return None

        return [h[0] for h in hits]  # Need only to return the first column
        

        

    def update_property(self,oldrec=None,newrec={}):

        self.log.debug("UPDATE PROP REC",oldrec)

        if "proptype" in newrec and oldrec["proptype"] != newrec["proptype"]:
            self.errors.append("UPDATE: Changing proptype is not allowed.")
            oldrec["internal"].append("UPDATE: Changing proptype is not allowed.")
            return None

        # Create the record for our replacement property
        finalrec={"proptype":oldrec["proptype"],
                  "creator":oldrec["creator"]}
        for k in ["from","to","value","complete"]:
            if k in newrec:
                finalrec[k]=newrec[k]
            elif k in oldrec:
                finalrec[k]=oldrec[k]

        if "to" in finalrec and "from" in finalrec and "value" in finalrec:
            del finalrec["value"]  # Can't be both link and literal

        if newrec.get("alive") == False:
            # This update is a property deletion
            finalrec["alive"] = False

        # Make the new property
        self.log.debug("MAKING REPLACEMENT PROP REC",oldrec)
        newp = prop.prop(rec=finalrec,db=self)
        if newp.is_valid:

            self.log.debug("CREATE UPDATED PROP:",finalrec)
            newp.create(is_update=True)
            if newp.errors:
                self.errors.append("PROPERTY UPDATE: "+("  ".join(newp.errors)))
                return None
            self.log.debug("CREATE UPDATED PROP FINAL:",newp.link["rec"])

            # Point old property to its replacement
            oldrec["internal"]["replaced_by"] = newp.link["guid"]
            #oldrec["internal"]["alive"] = False
            oldrec["replaced_by"] = newp.link["guid"]
            #oldrec["alive"] = False  -- Don't make old property dead
            oldrec["internal"]["rec"] = json.dumps(dict([(k,v) for k,v in oldrec.items() if k not in ["internal","rec"]]))
            # Update our index
            self.log.debug(oldrec)
            self.link_index.remove(key="replaced_by",entity=oldrec["internal"])
            self.link_index.add(key="replaced_by",value=newp.rec["guid"],entity=oldrec["internal"])

            #self.link_index.remove(key="alive",value="true",entity=oldrec["internal"])
            #self.link_index.add(key="alive",value="false",entity=oldrec["internal"])
            return newp
        else:
            self.errors.append("PROPERTY UPDATE: "+("  ".join(newp.errors)))
            oldrec["internal"].errors.append("PROPERTY UPDATE: "+("  ".join(newp.errors)))
            return None

               
        
    def destroy_node(self,n):
        n.delete()

    def destroy_link(self,n):
        l.delete()
        
        
        
                

                

                

        


        

    


