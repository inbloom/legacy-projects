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
import datetime,json

elapsed={}
started={}


class timer(object):

    def __init__(self, bin):
        self.bin = bin

    def __call__(self, f):
        def wrapped(*args,**kwds):
            global elapsed

            before = datetime.datetime.utcnow()
            result = f(*args,**kwds)
            after = datetime.datetime.utcnow()

            if self.bin not in elapsed:
                elapsed[self.bin] = {"time":0.0,"calls":0,"dist":[]}
            elapsed[self.bin]["time"] += (after - before).total_seconds()
            elapsed[self.bin]["calls"] += 1
            elapsed[self.bin]["dist"].append((after - before).total_seconds())
            return result

        return wrapped


def start(bin):
    global started
    started[bin] = datetime.datetime.utcnow()

def end(bin):
    global elapsed
    global started
    after = datetime.datetime.utcnow()
    if bin not in elapsed:
        elapsed[bin] = {"time":0.0,"calls":0,"dist":[]}
    elapsed[bin]["time"] += (after - started[bin]).total_seconds()
    elapsed[bin]["calls"] += 1
    #elapsed[bin]["dist"].append((after - started[bin]).total_seconds())
    del started[bin]

def profile():
    return json.dumps(elapsed,indent=4,sort_keys=True)
    
