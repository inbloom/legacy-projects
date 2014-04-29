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

import query_sequencer,sys,os,traceback,json

class regression(object):

    def __init__(self,working_dir=".",test_path="/test_suites/regression"):
        self.test_path = test_path
        self.working_dir = working_dir
        self.load_config()
        self.test_filenames = []
        self.find_tests()
        self.test_order = []
        self.errors = []
        self.result = {}
        self.complete_count = 0
        
    def load_config(self):
        try:
            self.config = json.loads(open(self.working_dir+"/lri_config.json").read())
        except:
            print "regression: COULD NOT LOAD '%s/lri_config.json'. USING DEFAULTS. %s" % (self.working_dir,traceback.format_exc())
            self.config = {"host":"localhost",
                           "port":8000}

    def find_tests(self):
        self.test_filenames = [fn for fn in os.listdir(self.working_dir+self.test_path) if (fn.endswith('.json') or fn.endswith('.yaml')) and '.report.' not in fn]
        self.test_filenames.sort()  # We always want to do the tests in the same order
        print len(self.test_filenames),"test sequences to run."

    def run_all(self):
        for fn in self.test_filenames:
            self.run_one(fn)
        print "\n%d (%.0f%%) out of %d test sequences successfully completed." % (self.complete_count,100.0*self.complete_count/len(self.test_filenames),len(self.test_filenames))
        if self.complete_count < len(self.test_filenames):
            print "Sequences that failed to complete:"
            for seq in self.test_order:
                if self.result[seq] != 'complete':
                    print "    -",seq

    def run_one(self,fn):
        qt = query_sequencer.query_sequencer(host=self.config['host'],
                                             port=self.config['port'],
                                             suitefilename=self.working_dir+self.test_path+"/"+fn)
        if qt.load():
            self.test_order.append(qt.stem)
            print "START test sequence: "+qt.stem+"......."
            qt.run()  # We log errors rather than allowing exceptions
            self.result[qt.stem]=qt.final_result['status']
            print "END test sequence: "+qt.stem+" with result ='"+self.result[qt.stem]+"'"
            if self.result[qt.stem] == 'complete':
                self.complete_count += 1
            qt.save_result()
            return True
        else:
            self.errors.extend(qt.errors)
            return False


if __name__=='__main__':

    if len(sys.argv) > 1:
        working_dir = sys.argv[1]
    else:
        working_dir = '.'

    r = regression(working_dir=working_dir)
    r.run_all()

        
        
