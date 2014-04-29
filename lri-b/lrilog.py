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

outfile = None

class lrilog(object):

    def __init__(self,name,outfilename=None,verbose=False):
        global outfile
        self.name = name
        self.outfilename = outfilename
        self.verbose = verbose
        if self.outfilename:
            if not outfile:
                self.open_logfile()


    def open_logfile(self):
        global outfile
        try:
            outfile = open(self.outfilename,'w')
        except Exception, e:
            pass

    def debug(self,*args):
        global outfile
        if self.verbose:
            try:
                print self.name + ":" + " ".join([str(a) for a in args])
            except:
                print self.name + ":" + " ".join([repr(a) for a in args])
                
        if outfile:
            try:
                outfile.write("%s : %s\n" % (self.name," ".join([str(a) for a in args])))
            except:
                outfile.write("%s : %s\n" % (self.name," ".join([repr(a) for a in args])))
                
            outfile.flush()
            
            
    
