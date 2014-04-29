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
import lridb,sys,neo4j,json,schema,subprocess,traceback,regression,neo_admin,os
import neorest

class lri_admin(object):

    def __init__(self,lri_dir):
        self.lri_dir=lri_dir
        self.config = json.loads(open(self.lri_dir+"/lri_config.json").read())
        self.errors=[]

    def init_db(self,boot=False,in_test_mode=False):
        self.db = neorest.neorest(config=self.config,create_indices=boot,in_test_mode=in_test_mode)

    def run(self,command,opt=None):
        na = neo_admin.neo_admin(neodir=self.config["neo4j_dir"],archive_dir=self.config.get("neo4j_archive_dir",self.config["neo4j_dir"]))

        if command == 'init_neo4j':
            na.prepare_fresh_install()

            if na.errors:
                print json.dumps(na.errors,indent=4,sort_keys=True)
                return False
            else:
                print json.dumps(na.log,indent=4,sort_keys=True)
                return True
            
        elif command =='start_neo4j':
            na.start()
            if na.errors:
                print json.dumps(na.errors,indent=4,sort_keys=True)
                return False
            else:
                print json.dumps(na.log,indent=4,sort_keys=True)
                return True
        
        elif command =='stop_neo4j':
            na.stop()
            if na.errors:
                print json.dumps(na.errors,indent=4,sort_keys=True)
                return False
            else:
                print json.dumps(na.log,indent=4,sort_keys=True)
                return True
        
        elif command =='take_snapshot':
            na.take_snapshot()
            if na.errors:
                print json.dumps(na.errors,indent=4,sort_keys=True)
                return False
            else:
                print json.dumps(na.log,indent=4,sort_keys=True)
                return True
        
        elif command =='restore_snapshot':
            na.restore_snapshot(name=opt)
            if na.errors:
                print json.dumps(na.errors,indent=4,sort_keys=True)
                return False
            else:
                print json.dumps(na.log,indent=4,sort_keys=True)
                return True
        
        elif command =='reset':
            # Deleting our database is really jsut restoring from a pristine database
            na.restore_snapshot(name='ORIG')
            if na.errors:
                print json.dumps(na.errors,indent=4,sort_keys=True)
                return False
            else:
                print json.dumps(na.log,indent=4,sort_keys=True)
                return True
        
        if command == 'create_lri':
            self.init_db(boot=True)
            print "NUMBER OF ENTITIES =",len(self.db.schema.index['id'])
            print "ERRORS FROM INITIALIZATION BOOTSTRAP:"
            for e in self.db.schema.errors:
                print "  - ",e
            print "WARNINGS FROM INITIALIZATION BOOTSTRAP:"
            for w in self.db.schema.warns:
                print "  - ",w
            if not self.db.schema.errors:
                self.db.schema.push_bootstrap_to_db(self.db)
                print "SCHEMA INDEX STATS:"
                for k,v in self.db.schema.index.items():
                    print k,"has size =",len(v)
            self.db.close()
            return True

        if command == 'start_lri':
           configfilename = self.lri_dir+"/lri_config.json"
           try:
               config = json.loads(open(configfilename).read())
           except:
               config = {}
           cmd = 'uwsgi --json "%s"' % (config.get("wsgi_config_filename",self.lri_dir+"/wsgi_config.json"))
           print "RUNNING WSGI SERVER WITH:",cmd
           print os.system(cmd)

        #elif command == 'delete':
        #    try:
        #        subprocess.check_output(['rm','-r',self.config['neo4j_dir'].strip()])
        #        subprocess.check_output(['mkdir',self.config['neo4j_dir'].strip()])
        #        return True
        #    except:
        #        self.errors.append("FAILED TO DELETE NEO4J DIR: "+traceback.format_exc())
        #        return False

        elif command == 'regression':
            print "Running Regression Tests...."
            try:
                r = regression.regression(working_dir=self.lri_dir)
                r.run_all()
                return True
            except:
                self.errors.append("REGRESSION TESTS EXPLODED: "+traceback.format_exc())
                return False 

        elif command == 'validate_bootstrap_schema':

            try:
                self.init_db(in_test_mode=True)
                s = self.db.schema 
                s.load_bootstrap()
                if self.db.errors or self.db.schema.errors:
                    self.errors.extend(["FAILED TO VALIDATE SCHEMA : "]+self.db.errors+self.db.schema.errors)
                    return False
                return True
            except:
                self.errors.extend(["SCHEMA VALIDATION EXPLODED: "]+traceback.format_exc().split("\n"))
                self.errors.extend(["FAILED TO VALIDATE SCHEMA : "]+self.db.errors+self.db.schema.errors)
                return False

        elif command == 'validate_live_schema':

            try:
                self.init_db(in_test_mode=False)
                if self.db.errors or self.db.schema.errors:
                    self.errors.extend(["FAILED TO VALIDATE SCHEMA : "]+self.db.errors+self.db.schema.errors)
                    return False
                return True
            except:
                self.errors.extend(["SCHEMA VALIDATION EXPLODED: "]+traceback.format_exc().split("\n"))
                self.errors.extend(["FAILED TO VALIDATE SCHEMA : "]+self.db.errors+self.db.schema.errors)
        else:
            print "Unknown Command: ",command
            

    def print_rels(self):
        for r in self.db.ndb.relationships:
            rp = dict([(k,v) for k,v in r.items()])
            print repr(rp)

    def print_nodes(self):
        for r in self.db.ndb.nodes:
            rp = dict([(k,v) for k,v in r.items()])
            print "--------------------------------------------------------------------"
            print repr(rp)

    

if __name__=='__main__':
    la = lri_admin(".")
    if len(sys.argv) > 2:
        opt = sys.argv[2]
    else:
        opt = 'rest'
    la.run(sys.argv[1],opt=opt)
    print "NUMBER OF ERRORS FOUND =",len(la.errors)
    if la.errors:
        print "ERRORS:",json.dumps(la.errors)


    
