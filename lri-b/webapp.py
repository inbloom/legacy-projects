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
import sys,json,web,cgi,traceback,datetime,urlparse,os

# To allow imports of lri source files
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)
import request,cache,neorest

default_headers = [('Content-Type', 'application/json')]

class index(object):

    def GET(self):
        return self._process_request('GET')

    def POST(self):
        return self._process_request('POST')

    def _assemble_redirect(self,q,opts):

        global config
        
        query = q
        target_key = opts.get("target")
        target_prefix = config.get("external_search_servers",{}).get(target_key)

        if not target_key or not target_prefix:
            web.ctx.status = "404 Not Found"
            web.header('Content-Type', 'application/json',unique=True)
            return {"status":"error",
                    "message":"External server target '%s' cannot be found." % (target_key)}

        web.ctx.status = "302 Found"
        web.header('Location',"%s %s " %(target_prefix,query))
        return {}

    def _process_request(self,mode):

        global config
        global ext_cache
        global db

        path = web.ctx.env.get('PATH_INFO', '').lstrip('/')
        get_params = web.ctx.query[1:]
        post_data = web.data()[1:]
        web.header('Content-Type', 'application/json',unique=True)

        if path not in ['entity/search','entity/create','property/create','property/update']:
            web.ctx.status = "404 Not Found"
            
        if mode == 'POST':
            query = post_data
        elif mode == 'GET':
            query = get_params
        else:
            web.ctx.status = "405 Method Not Allowed"
            return {"status":"error",
                    "message":"Only GET and POST are supported, not '%s'" % (web.ctx.method)}

        print  "QUERY",query
        try:
            parsed_query = urlparse.parse_qs(query)
        except Exception, e:
            web.ctx.status = "400 Bad Request"
            return json.dumps({"status":"error",
                               "message":["Query not properly URI encoded"]+traceback.format_exc().split("\n")},indent=4,sort_keys=True)

        try:
            if 'q' in parsed_query:
                q = cgi.escape(parsed_query['q'][0])
            else:
                q = ''
            if 'opts' in parsed_query:
                opts = cgi.escape(parsed_query['opts'][0])
            else:
                opts = '{}'
        except Exception, e:
            web.ctx.status = "400 Bad Request"
            return json.dumps({"status":"error",
                               "message":["Query not properly URI encoded"]+traceback.format_exc().split("\n")},indent=4,sort_keys=True)
                               

        try:
            options = json.loads(opts)
            if "format" in options:
                if options["format"]=="xml":
                    web.header('Content-Type', 'text/xml',unique=True)
                elif options["format"]=="json":
                    web.header('Content-Type', 'application/json',unique=True)
                elif options["format"]=="yaml":
                    web.header('Content-Type', 'text/x-yaml',unique=True)
                else:
                    web.header('Content-Type', 'application/json',unique=True)
            else:
                web.header('Content-Type', 'application/json',unique=True)
        except Exception, e:
            web.header('Content-Type', 'application/json',unique=True)

        try:
            q_decoded = json.loads(q)
        except:
            web.ctx.status = "400 Bad Request"
            return json.dumps({"status":"error",
                               "message":["Bad JSON in 'q'"]},indent=4,sort_keys=True)
            q_decoded = {}

        try:
            opts_decoded = json.loads(opts)
        except Exception, e:
            web.ctx.status = "400 Bad Request"
            return json.dumps({"status":"error",
                               "message":"Bad JSON in 'opts'"},indent=4,sort_keys=True)
            opts_decoded = {}

        if 'external/search' in path:
            return _process_redirect(q_decoded,opts_decoded)

        req  = request.request(action=path,q=q_decoded,opts=opts_decoded,db=db,ext_cache=ext_cache)

        request_success = req.perform_request()

        if opts_decoded.has_key("format"):
            resp = req.response_string(format=opts_decoded["format"])
        else:
            resp = req.response_string()

        if opts_decoded.has_key("format"):
            resp = req.response_string(format=opts_decoded["format"])
        else:
            resp = req.response_string()

        web.ctx.status = req.http_status

        return resp
        

class webapp(object):

    def __init__(self,configfilename):
        #self.configfilename = configfilename
        #self.config = json.loads(open(self.configfilename).read())
        #global config
        #config.update(self.config)
        self.app = app = web.application(['/.*','index'], globals())

    def run(self):
        self.app.run()


######################################################################
# Everything starts here
######################################################################
        
configfilename = current_dir+'/lri_config.json'
if len(sys.argv) > 1:
    configfilename = sys.argv[1]

#  Try to setup server
valid_setup = True
try:
    config = json.loads(open(configfilename).read())
    try:
        ext_cache = cache.make_cache(config)
        try:
            db = neorest.neorest(config=config,create_indices=False)
        except Exception, e:
            print "UNABLE TO SETUP NEO4J DATABASE!"
            print traceback.format_exc()
            valid_setup = False
    except:
        print "UNABLE TO SET UP CACHE"
        valid_setup = False
except Exception, e:
    print "UNABLE TO PARSE CONFIG FILE:",configfilename
    valid_setup = False

if valid_setup:
    if __name__ == "__main__":
        # Local execution
        wa = webapp(configfilename)
        wa.run()
    else:
        # WSGI for nginx
        wa = webapp(configfilename)
        application = wa.app.wsgifunc()


