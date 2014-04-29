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
import json,hashlib,datetime
try:
    import memcache
    memcached_exists = True
except:
    memcached_exists = False

cache = {}

def now():
    return datetime.datetime.utcnow().isoformat()

def make_cache(config):
    if config.get('cache_type') == 'local':
        return local_cache()
    elif config.get('cache_type') == 'memcached':
        if not memcached_exists:
            print "Memcached not installed!"
            return None
        if config.get('memcached_host') and config.get('memcached_port'):
            return memcached_cache(host=config['memcached_host'],port=config['memcached_port'])
        else:
            return None
        
def make_key(k):
    try:
        print "CACHE HASH:",json.dumps(k,sort_keys=True)
        return hashlib.md5(json.dumps(k,sort_keys=True)).hexdigest()
    except:
        # If we get here, our key may not be stable
        return hashlib.md5(repr(k)).hexdigest()

def make_value(v):
    return json.dumps({"timestamp": datetime.datetime.utcnow().isoformat(),"value":v},
                      sort_keys=True)

def parse_value(v):
    try:
        return json.loads(v)
    except:
        return v

class lri_cache(object):

    def write_value(self,v):
        try:
            k = make_key(v)
            self.write_pair(k,v)
            return k
        except:
            return False



class local_cache(lri_cache):

    def __init__(self):
        self.cache = cache

    def read(self,k):
        return parse_value(self.cache.get(k,'null'))

    def write_pair(self,k,v):
        try:
            self.cache[k] = make_value(v)
            return True
        except:
            return False

    def delete(self,k):
        if k in self.cache:
            del self.cache[k]
            return True
        else:
            return False

    def clear(self):
        self.cache={}

class memcached_cache(lri_cache):

    def __init__(self,host=None,port=None):
        self.cache = memcache.Client([host+':'+str(port)])

    def read(self,k):
        return parse_value(self.cache.get(k.encode('utf-8')))

    def write_pair(self,k,v):
        self.cache.set(k.encode('utf-8'),make_value(v))
        return True

    def delete(self,k):
        pass

    def clear(self):
        self.cache.flush_all()


if __name__=='__main__':
    config = json.loads(open('./lri_config.json').read())
    c = make_cache(config)
    print "Cache is of class:",c.__class__
    k = c.write_value({"a":1,"b":2})
    print "Key is:",k
    print c.read(k)





    
    
