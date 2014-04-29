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

import sys,json,datetime,commands


class neo_admin(object):

    def __init__(self,neodir=".",archive_dir=None):
        self.dir = neodir
        if not archive_dir:
            self.archive_dir = self.dir
        else:
            self.archive_dir = archive_dir
        self.errors = []
        self.log = []
        self.latest = 'NONE'
        self.status = 'NEW'

    def shell(self,cmd,error_msg=None):
        if not error_msg:
            error_msg="Error running shell command '%s'" % (cmd)

        print "SHELL:",cmd
        (exitstatus, out) = commands.getstatusoutput(cmd)
        print "SHELL OUTPUT:",out,exitstatus
        if exitstatus == 0:
            return {'success':True,'output':out}
        else:
            self.errors.append(error_msg)
            return {'success':False,'output':out}

    def prepare_fresh_install(self):

        # Move the original, clean data dir
        if self.shell('mv "%s/data" "%s/data.LIVE" ' % (self.dir,self.archive_dir),
                      "Could not move fresh neo4j data directory")['success'] == False:
            return False

        # Link the apparent default location data dir to the LIVE one in the archive
        if self.shell('ln -s "%s/data.LIVE" "%s/data"' % (self.dir,self.archive_dir),
                      "Could not make data dir symlink %s/data.LIVE" % (self.archive_dir))['success'] == False:
            return False

        # Make a backup of our tabla rasa
        if not self.take_snapshot(name="ORIG",restart=False):
            return False


        self.status = "INITIALIZED"
        return True
        
    def get_all_data_dirs(self):
        self.datadirs = os.listdir(self.archive_dir)

    def start(self):
        result = self.shell("%s/bin/neo4j start" % (self.dir))
        if result['success'] == False:
            self.errors.append(result['output'].split("\n"))
            return False
        self.status = "RUNNING"
        return result['output']

    def stop(self):
        result = self.shell("%s/bin/neo4j stop" % (self.dir))
        if result['success'] == False:
            self.errors.append(result['output'].split("\n"))
            return False
        self.status = "STOPPED"
        return result['output']


    def take_snapshot(self,name=None,restart=True):
        if self.status != 'STOPPED':
            self.stop()
        if self.status == 'RUNNING':
            self.errors.append("Cannot stop server for backup")
            return False
        if not name:
            name = datetime.datetime.utcnow().isoformat()[0:19]

        result = self.shell("cp -pr %s/data.LIVE %s/data.snapshot.%s" % (self.dir,self.archive_dir,name))
        if result['success'] == False:
            self.errors.append(result['output'].split("\n"))
            self.errors.append("Could not take snapshot to '%s/data.%s'" % (self.archive_dir,name))
            return False

        # Restart our server and return name of snapshot
        if restart:
            self.start()
        self.latest = name
        self.log.append("SNAPSHOT TAKEN --> %s" % (name))
        return name


    def delete_live(self,is_part_of_restore=False):
        now = datetime.datetime.utcnow().isoformat()[0:19]
        
        result = self.shell("mv %s/data.LIVE %s/DELETED_AT.%s" % (self.archive_dir,self.archive_dir,now))
        if result['success'] == False:
            self.errors.append(result['output'].split("\n"))
            self.errors.append("Could not delete live datadir to DELETED_AT.%s'" % (now))
            return False
        self.log.append("LIVE deleted ---> DELETED_AT.%s" % (now))
        self.latest = "NONE"
        return True


    def restore_snapshot(self,name):
        if self.status != 'STOPPED':
            self.stop()
        if self.status == 'RUNNING':
            self.errors.append("Cannot stop server for backup")
            return False

        if not self.delete_live():
            return False
        
        result = self.shell("cp -pr %s/data.snapshot.%s %s/data.LIVE" % (self.archive_dir,name,self.archive_dir))
        if result['success'] == False:
            self.errors.append(result['output'].split("\n"))
            self.errors.append("Could not restore snapshot %s'" % (name))
            return False

        # Restart our server
        self.start()
        self.latest = name
        self.log.append("SNAPSHOT RESTORED <--- %s" % (name))
        return True


    
