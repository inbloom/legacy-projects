#!/usr/bin/python

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

from bs4 import BeautifulSoup
import copy
import json
import operator
import re
import requests
import sys
import traceback
import urllib
import web
from xml.sax import saxutils

import httpconfig
import utils

from ccss import format
from ccss import insert
from ccss import prune
from ccss import query
from ccss import sort

"""LRI interface."""

class NotImplementedError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class WrongTypeError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class DebugMessage(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class DeprecatedError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

##### web.py
web.config.debug = True
urls = ("/.*", "ccss")

app = web.application(urls, globals())
application = app.wsgifunc()

class index:
    def GET(self):
        return "hello, world!"

class ccss:
    def start_response(self, status, headers):
        web.ctx.status = status
        for header, value in headers:
            web.header(header, value)

    def convertQueryString(self):
        """Converts &-separated query string to LRI-style json-formatted opts

?key1=val1&key2=val2 -> ?opts={"key1":"val1","key2":"val2"}

"""

        queryString = web.ctx.env.get("QUERY_STRING", "")
        queryVars = queryString.split("&")

        emptyOpts = '"opts={}"'
        if len(queryVars) == 0:
            return emptyOpts
        if queryString.find("=") == -1:
            return emptyOpts

        opts = {}
        try:
            web.debug("convertQueryString: queryString = %s" % queryString)
            web.debug("convertQueryString: queryVars = %s" % queryVars)

            for var in queryVars:
                var = var.strip("?")
                key, val = var.split("=")
                if val in ["true", "True"]:
                    val = True
                if val in ["false", "False"]:
                    val = False
                if key in opts:
                    opts[key].append(val)
                else:
                    opts[key] = []
                    opts[key].append(val)

            for key in opts:
                if len(opts[key]) == 1:
                    val = opts[key][0]
                    opts[key] = val
        except Exception, e:
            web.debug("convertQueryString: %r" % e)

        s = "opts=%s" % json.dumps(opts)
        return s
        
    def GET(self, extra=None):
        """Entry point for HTTP GET"""

        web.debug("GET")

        web.debug("web.config: ")
        for config in web.config:
            try:
                web.debug("    %s : %s" % (config, web.config[config]))
            except ValueError, e:
                web.debug("GET: Caught ValueError: config: %r" % config)

        web.debug("web.config[session_parameters]: ")
        for param in web.config["session_parameters"]:
            try:
                web.debug("    %s : %s" % (param, web.config["session_parameters"][param]))
            except ValueError, e:
                web.debug("GET: Caught ValueError: param: %r" % param)

        web.debug("web.ctx.env: ")
        web.debug(web.ctx.env)

        if web.ctx.env["QUERY_STRING"].find("opts={") == -1:
            web.ctx.env["QUERY_STRING"] = self.convertQueryString()

        return getApplication(web.ctx.env, self.start_response)

    def POST(self, extra=None):
        """Entry point for HTTP POST"""

        web.debug("POST")

        # Convert query str to opts
        web.ctx.env["QUERY_STRING"] = self.convertQueryString()
        web.debug("QUERY_STRING: %s" % web.ctx.env["QUERY_STRING"])

        # Print env
        web.debug("web.ctx.env: ")
        web.debug(web.ctx.env)

        # Print POST data dict
        web.debug("web.input: ")
        userData = web.input()
        web.debug(userData)

        # Print encoded POST data
        web.debug("web.data: ")
        rawData = web.data()
        web.debug(rawData)

        # Set headers to send back to client
        #web.header("Content-Type", "application/xml; charset=utf-8")
        web.header("Access-Control-Allow-Origin", "*")

        # Return data to client
        return postApplication(web.ctx.env, self.start_response, userData)

def getUrnJson(data):
    """Returns URN to entity in JSON data"""

    decodedJson = json.loads(data)
    return decodedJson["urn:lri:property_type:id"]

def getUrnXml(data):
    """Returns URN to entity in XML data"""

    xml = saxutils.unescape(data)
    soup = BeautifulSoup(xml)
    return soup.find(key="urn:lri:property_type:id").getText().strip()

def postApplication(environ, start_response, userData):
    """web.py application to do HTTP POST"""

    web.debug("postApplication")

    status = 0
    result = []

    pathInfo  = environ["PATH_INFO"]
    web.debug("postApplication: pathInfo = %s" % pathInfo)
    web.debug("postApplication: userData = %r" % userData)
    web.debug("postApplication: web.input() = %r" % web.input())
    web.debug("postApplication: web.data() = %r" % web.data())

    web.debug("postApplication: userData.keys() = %r" % userData.keys())

    decodedOpts = {}
    code = None
    if environ.has_key("QUERY_STRING"):
        decodedOpts = decodeOpts(environ["QUERY_STRING"])
        web.debug("postApplication: decodedOpts = %r" % decodedOpts)
    if environ["REQUEST_METHOD"] == "POST":
        code, result = doPost(pathInfo, decodedOpts, userData.data)
    else:
        return result

    status = ""
    if code == 201:
        status = "201 Created"
    elif code == 404:
        status = "404 Not Found"
    elif code == 500:
        status = "500 Internal Server Error"
    else:
        # pywebapp.py returns 200 OK for GET & POST
        if code == 200:
            status = "201 Created"

    # Access-Control-Allow-Origin 
    # is needed to serve cross-domain JS
    headers = [
        ("X-Powered-By", "Python"),
        ("Webapp", "ccss"),
        ("Access-Control-Allow-Origin", "*")]

    if code in [404, 500]:
        start_response(status, headers)
        result = status + "\n\n" + pathInfo + "\n\n" + result
        web.debug("postApplication: ERROR: Returning code: %d" % code)
        web.debug("postApplication: ERROR: Returning headers: %r" % headers)
        return result

    toFormat = "xml"
    if decodedOpts.has_key("format"):
        toFormat = decodedOpts["format"]
    elif userData.has_key("format"):
        toFormat = userData.format

    if toFormat == "json":
        headers.append(("Content-Type", "application/json; charset=utf-8"))
    elif toFormat in ["xml", "johnxml", "oldxml"]:
        headers.append(("Content-Type", "application/xml; charset=UTF-8"))
    elif toFormat == "yaml":
        headers.append(("Content-Type", "text/x-yaml; charset=utf-8"))
    else:
        headers.append(("Content-Type", "application/json"))
    
    # Add Location header
    if toFormat in ["json", "xml"]:
        uri = ""
        if toFormat == "json":
            uri = getUrnJson(userData.data)
        elif toFormat == "xml":
            uri = getUrnXml(userData.data)
        #headers.append(("Location", uri))

    web.debug("postApplication: Returning status: %s" % status)
    web.debug("postApplication: Returning headers: %r" % headers)
    web.debug("postApplication: Returning result: ")
    if toFormat == "xml":
        try:
            xml = saxutils.unescape(result)
            soup = BeautifulSoup(xml)
            print(soup.prettify())
        except AttributeError, e:
            print("Error printing xml")
            print(e)
            print(result)

    start_response(status, headers)

    return result


def doPost(pathInfo, opts, data):
    """Does HTTP POST"""

    web.debug("doPost")

    formatted = ""
    results = QueryResult()
    code = 201
    try:
        # Create & run inserts (create, update)
        toFormat = "xml"
        if not "format" in opts:
            userData = web.input()
            toFormat = userData.get("format", "xml")
        web.debug("to format = %s" % toFormat)

        pattern = "(/[a-z_]+)(/[a-z]+)"
        m = re.match(pattern, pathInfo)
        ccssType, action = m.groups()
        if action == "/create":
            i = insert.InsertFactory().CreateInsert(ccssType, action, opts, data)
            for url in i.getUrls():
                r = QueryRunner(url)
                results = r.runQuery()
                if not isinstance(results, QueryResult):
                    raise WrongTypeError("doPost: QueryRunner.runQuery(): expected QueryResult, got %s" % type(results))
            code = results.getHttpStatusCode()

            # Convert to requested format
            f = format.FormatterFactory().CreateFormatter(toFormat)
            formatted = f.format(results.getData())

        elif action == "/update":
            web.debug("===== %s =====" % action)

            updates = insert.parseXml(data)
            web.debug("doPost: updates = %r" % updates)

            responses = insert.runUpdates(updates, opts)
            count = 0
            for r in responses:
                f = format.FormatterFactory().CreateFormatter(toFormat)
                formatted += f.format(utils.getJson(r))

                # What to do about multiple <?xml...?> lines?
                #tmp = f.format(r.json)
                #if count > 0:
                #    if toFormat in ["xml", "johnxml", "oldxml"]:
                #        lines = tmp.split("\n")
                #        lines.remove(lines[0])
                #        tmp = "\n".join(lines)
                #formatted += tmp
                #count += 1

    except NotImplementedError, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted = "doPost: Caught NotImplementedError: " + str(e) + "\n"
        formatted += "-" * 60 + "\n"
        formatted += traceback.format_exc()
        formatted += "-" * 60 + "\n"
        code = 501

    except WrongTypeError, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted = "doPost: Caught WrongTypeError: " + str(e) + "\n"
        formatted += "-" * 60 + "\n"
        formatted += traceback.format_exc()
        formatted += "-" * 60 + "\n"
        code = 500

    except Exception, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted = "doPost: Caught Exception: " + str(e) + "\n"
        formatted += "-" * 60 + "\n"
        formatted += traceback.format_exc()
        formatted += "-" * 60 + "\n"
        code = 500
        
    return code, formatted

def getApplication(environ, start_response):
    """web.py application for doing HTTP GET"""

    web.debug("getApplication")

    status = 0
    result = []

    pathInfo = environ["PATH_INFO"]
    decodedOpts = {}
    if environ.has_key("QUERY_STRING"):
        web.debug("QUERY_STRING = %s" % environ["QUERY_STRING"])
        decodedOpts = decodeOpts(environ["QUERY_STRING"])
        web.debug("decodedOpts = %r" % decodedOpts)
    if environ["REQUEST_METHOD"] == "GET":
        code, result = doGet(pathInfo, decodedOpts)
    else:
        return result

    status = code
    if code == 200:
        status = "200 OK"
    elif code == 404:
        status = "404 Not Found"
    elif code == 500:
        status = "500 Internal Server Error"

    # Access-Control-Allow-Origin 
    # is needed to serve cross-domain JS
    headers = [
        ("X-Powered-By", "Python"),
        ("Webapp", "ccss"),
        ("Access-Control-Allow-Origin", "*")]

    if "format" in decodedOpts:
        if decodedOpts["format"] == "json":
            headers.append(("Content-Type", "application/json"))
        elif decodedOpts["format"] in ["xml", "johnxml", "oldxml"]:
            headers.append(("Content-Type", "application/xml"))
        elif decodedOpts["format"] == "yaml":
            headers.append(("Content-Type", "text/x-yaml"))
        else:
            headers.append(("Content-Type", "application/json"))

    start_response(status, headers)

    if code in [404, 500]:
        result = status + "\n\n" + pathInfo + "\n\n" + result

    return result

def decodeOpts(opts):
    """Decodes options string to dict"""

    decodedOpts = {}
    try:
        print("decodeOpts: opts = %s" % opts)
        parts = opts.split("opts=")
        print("decodeOpts: opts = %r" % opts)
        print("decodeOpts: parts[1] = %r" % parts[1])
        decodedOpts = json.loads(str(parts[1]))
        print("decodeOpts: decodedOpts = %r" % decodedOpts)
    except Exception, e:
        web.debug("decodeOpts: Caught Exception: %r" % e)
        pass

    return decodedOpts

def doGet(pathInfo, opts):
    """Does HTTP GET"""

    web.debug("doGet")

    # Quick /entity/search for property:value
    # Looks up entity and returns
    if pathInfo == "/get":
        httpConfig = httpconfig.HttpConfig(web.ctx.env["DOCUMENT_ROOT"])
        host = httpConfig.config["serverhost"]
        port = httpConfig.config["serverport"]
        prop = "urn:lri:property_type:id"
        val = opts["id"]
        url = 'http://%s:%s/entity/search?q={"%s":"%s"}&opts={}' % (host, port,
                                                                    prop, val)
        web.debug("doGet: url = " + url)
        r = requests.get(url)
        
        text = None
        try:
            text = r.content
        except AttributeError, e:
            print("doGet: No content")

            try:
                text = r.text
            except AttributeError, e:
                print("doGet: No text")

        if text is None:
            raise Exception("Could not get text from requests response")

        return r.status_code, text
                                                             

    formatted = ""
    results = None
    code = 200
    try:
        # Create & run query
        httpConfig = httpconfig.HttpConfig(web.ctx.env["DOCUMENT_ROOT"])

        toFormat = "json"
        if "format" in opts:
            toFormat = opts["format"]
            del opts["format"]

        # Set to True for paging
        doPageResults = False

        if doPageResults:
            # Size of result set returned w/cursor
            limit = 1

            q = query.QueryFactory().CreateQuery(pathInfo, opts, httpConfig, limit)
            if q is None:
                code = 404
                return code, formatted

            # Run query once w/small limit
            # Extract cursor from results
            # Run subsequent queries in loop
            #   until cursor comes back False
            print("doGet: url = %s" % q.getUrl())
            response = requests.get(q.getUrl())

            j = utils.getJson(response)
            if "cursor" in j:
                cursor = j["cursor"]
                print("\ndoGet: cursor = %s\n" % cursor)
                statusCode = response.status_code
                status = json.dumps(j["status"])
                items = []
                if cursor is False:
                    items = j["response"]
                else:
                    count = 0
                    while cursor is not False: # != "false":
                        print("doGet:   Count = %d" % count)
                        print("doGet:   Getting next %d results" % limit)

                        url = 'http://%s:%s/entity/search?q={"limit":%d,"cursor":%s}&opts=%s' % (httpConfig.config["serverhost"], 
                                                                                                 httpConfig.config["serverport"],
                                                                                                 limit, json.dumps(cursor),
                                                                                                 json.dumps(opts))

                        print("doGet:   url = %s" % url)

                        r = requests.get(url)
                        statusCode = r.status_code
                        try:
                            utils.getJson(r)
                        except Exception(e):
                            print utils.getText(r)
                            continue

                        cursor = j["cursor"]
                        status = j["status"]

                        print("doGet:   Got %d results" % len(j["response"]))
                        for item in j["response"]:
                            itemId = item["props"]["urn:lri:property_type:id"]
                            # XXX: should this be: if item in items?
                            if item in items:
                                print("doGet:     DUPLICATE: %s" % itemId)
                            else:
                                items.append(item)
                        count += 1
                    print("doGet: Got %d items: " % len(items))
                    for i in items:
                        print("doGet:   %s" % i["props"]["urn:lri:property_type:id"])

                    resp = {}
                    resp["response"] = items
                    resp["status"] = status
                    results = QueryResult(statusCode, resp)
        else:
            # Create a Query
            limit = None
            if pathInfo == "/competency_paths":
                limit = 100
            q = query.QueryFactory().CreateQuery(pathInfo, opts, httpConfig, limit=limit)
            if q is None:
                code = 404
                return code, formatted

            # Run the Query
            r = QueryRunner(q.getUrl())
            print("\ndoGet: Running query: ")
            print("    query = %s" % q.getUrl())

            if pathInfo == "/standards":
                results = q.getStandards()
                results = QueryResult(results["status_code"], results)
                # Don't prune
                opts["prune"] = False
            else:
                results = r.runQuery()
            print("\ndoGet: Ran query")

        if not isinstance(results, QueryResult):
            raise WrongTypeError("doGet: QueryRunner.runQuery(): expected QueryResult, got %s" % type(results))
        code = results.getHttpStatusCode()

        # Prune results by default
        if not "prune" in opts or opts["prune"] is not False:
            opts["prune"] = True

        if not "sort" in opts:
            opts["sort"] = True

        web.debug("doGet: prune = %s" % opts["prune"])
        web.debug("doGet: sort = %s" % opts["sort"])

        # Prune results
        # Arrange response from LRI, possibly discarding extra data
        if "prune" in opts and opts["prune"] is True:
            print("\ndoGet: Pruning ...\n")

            # Get a Pruner
            p = prune.PrunerFactory().CreatePruner(pathInfo, opts)
            filterBy = opts.get("property", [])

            # Prune, keeping any optional filtered properties
            results = p.prune(results, keep=filterBy)

            if len(filterBy) > 0:
                # Filter
                if not isinstance(filterBy, list):
                    filterBy = [filterBy]
                key = pathInfo.strip("/")
                results.filterPruned(filterBy, key)

                # Sort
                if "sort" in opts and opts["sort"] is True:
                    # Get a Sorter
                    s = sort.FilterSorter(key, filterBy[0])

                    # Sort
                    results = s.sort(results)
            else:
                # Sort
                # Default behavior is to sort results
                if "sort" in opts and  opts["sort"] is True:
                    # Get a Sorter
                    s = sort.SorterFactory().CreateSorter(pathInfo, results)

                    # Sort
                    results = s.sort(results)
            print("\ndoGet: Done pruning\n")
        else:
            # Sort
            # Default behavior is to sort results
            if "sort" in opts and  opts["sort"] is True:
                # Get a Sorter
                s = sort.SorterFactory().CreateSorter(pathInfo, results)

                # Sort
                results = s.sort(results)
        print("\ndoGet: Done sorting\n")

        # Convert to requested format
        print("\nFormatting to: %s ..." % toFormat)

        # Get a Formatter
        f = format.FormatterFactory().CreateFormatter(toFormat)

        # Format to requested format
        # Default is JSON
        formatted = f.format(results.getData())
        print("\nDone formatting")

    except NotImplementedError, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted = "doGet: Caught NotImplementedError: " + str(e) + "\n"
        formatted += "-" * 60 + "\n"
        formatted += traceback.format_exc()
        formatted += "-" * 60 + "\n"
        code = 501

    except WrongTypeError, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted = "doGet: Caught WrongTypeError: " + str(e) + "\n"
        formatted += "-" * 60 + "\n"
        formatted += traceback.format_exc()
        formatted += "-" * 60 + "\n"
        code = 500

    except Exception, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted = "doGet: Caught Exception: " + str(e) + "\n"
        formatted += "-" * 60 + "\n"
        formatted += traceback.format_exc()
        formatted += "-" * 60 + "\n"
        code = 500
        
    return code, formatted

class QueryRunner(object):
    """Class for running an LRI query"""

    def __init__(self, url):
        self.url = url

    def runQuery(self):
        """Runs the query. Returns QueryResult"""

        msg = "QueryRunner.runQuery: url = %s" % self.url
        web.debug(msg)

        r = requests.get(self.url)
        queryResult = QueryResult(r.status_code, utils.getJson(r))
                 
        return queryResult

class QueryResult(object):
    """Holds result of LRI query."""

    def __init__(self, code=None, results={}):
        self.code = code

        # self.data is a dict
        self.data = results
        if not isinstance(self.data, dict):
            raise WrongTypeError("results arg must be a dict, not", type(self.data))

        # valid keys into self.data dict
        self.validKeys = ["api_version",
                          "opts",
                          "q",
                          "response",
                          "status", 
                          "timer", 
                          "timestamp"]

        self.entityKey = None

    def getHttpStatusCode(self):
        """Returns HTTP status code."""

        return self.code

    def get(self, key=None):
        """Returns key in dict. See self.validKeys"""

        if key == None:
            return self.data

        if key not in self.validKeys:
            return self.data

        if self.data is None:
            return None

        if key not in self.data:
            return ""

        return self.data[key]

    def getData(self):
        """Returns query response data dict."""

        return self.data

    def getStatus(self):
        """Requery query response status."""

        return self.get("status")

    def getPropertyNames(self):
        """Returns property names

Use to return properties for certain type
/ccss/TYPES/property_names

Properties can be used to filter out un-wanted properties
"""

        propertyNames = []
        try:
            for i in xrange(1):
                propertyNames = self.get("response")[i]["props"].keys()

            for entity in self.get("response"):
                key = "urn:lri:property_type:properties"
                if key in entity["props"]:
                    for propertyName in entity["props"][key]:
                        if propertyName not in propertyNames:
                            propertyNames.append(propertyName)

            for entity in self.get("response"):
                key = "urn:lri:property_type:specific_properties"
                if key in entity["props"]:
                    if isinstance(entity["props"][key], list):
                        for propertyName in entity["props"][key]:
                            if propertyName not in propertyNames:
                                propertyNames.append(propertyName)
                    elif isinstance(entity["props"][key], str):
                        if propertyName not in propertyNames:
                            propertyNames.append(entity["props"][key])
                    
        except KeyError, e:
            # Results have been pruned
            web.debug("QueryResult.getPropertyNames: %r" % e)
            for response in self.get("response"):
                propertyNames = response["property_names"]

        return propertyNames

    def getDefaultFilterProps(self):
        return ["urn:lri:property_type:id"]

    def filter(self, properties):
        """Returns data w/all keys removed but id and given properties"""

        # Get all properties
        props = []
        for item in self.get("response"):
            props = item["props"].keys()

        # Keep props we want to keep
        # Start with props that are never removed
        # Add props passed in
        keeps = self.getDefaultFilterProps()
        for prop in properties:
            if prop not in keeps:
                keeps.append(prop)

        # Remove props we want to keep from list
        for keep in keeps:
            try:
                props.remove(keep)
            except ValueError, e:
                web.debug("%s: %r" % (keep, e))

        # Remove props we don't want to keep
        for item in self.get("response"):
            for prop in props:
                try:
                    del item["props"][prop]
                except ValueError, e:
                    web.debug("QueryResult.filter: %s: %r" % (entityId, e))
                except KeyError, e:
                    web.debug("QueryResult.filter: %s: %r" % (entityId, e))

    def filterPruned(self, properties, key):
        """Returns data w/all keys removed but id and given properties

Works on filtered results

"""
        # Get all properties
        props = []
        for item in self.get("response"):
            for i in item[key]:
                for prop in i["props"].keys():
                    if prop not in props:
                        props.append(prop)

        # Keep props we want to keep
        # Start with props that are never removed
        # Add props passed in
        keeps = self.getDefaultFilterProps()
        for prop in properties:
            if prop not in keeps:
                keeps.append(prop)

        # Remove props we want to keep from list
        for keep in keeps:
            try:
                props.remove(keep)
            except ValueError, e:
                web.debug("QueryResult.filterPruned: %s: %r" % (keep, e))

        # Remove props we don't want to keep
        for item in self.get("response"):
            for i in item[key]:
                entityId = i["props"]["urn:lri:property_type:id"]
                for prop in props:
                    try:
                        del i["props"][prop]
                    except ValueError, e:
                        web.debug("QueryResult.filterPruned: %s: %r" % (entityId, e))
                    except KeyError, e:
                        web.debug("QueryResult.filterPruned: %s: %r" % (entityId, e))

    def set(self, key, value):
        """Sets key in dict. See self.validKeys"""

        if not key in self.validKeys:
            return

        self.data[key] = value

    def setData(self, value):
        """Sets query response data (as in sorting)."""

        self.data = value

##### web.py
if __name__ == '__main__':
    web.debug(__name__)
    app.run()
