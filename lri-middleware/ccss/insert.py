###############################################################################
# Insert
###############################################################################

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
import json
import os.path
import random
import requests
import web
from xml.sax import saxutils

import httpconfig

class InsertFactory(object):
    def CreateInsert(self, ccssType, action, opts, data):
        web.debug("CreateInsert")
        web.debug("    ccssType=%s" % ccssType)
        web.debug("    action=%s" % action)
        web.debug("    opts=%r" % opts)
        web.debug("    data=%r" % data)

        web.debug("CreateInsert: ")
        web.debug("CreateInsert:    data = %s" % data)
        print("CreateInsert:    data = %s" % data)

        insert = None
        if ccssType == "/initiative":
            if action == "/create":
                insert = InitiativeCreate(opts, data)
            elif action == "/update":
                insert = InitiativeUpdate(opts, data)
            
        elif ccssType == "/framework":
            if action == "/create":
                insert = FrameworkCreate(opts, data)
            elif action == "/update":
                insert = FrameworkUpdate(opts, data)

        elif ccssType == "/set":
            if action == "/create":
                insert = SetCreate(opts, data)
            elif action == "/update":
                insert = SetUpdate(opts, data)

        elif ccssType == "/grade_level":
            if action == "/create":
                insert = GradeCreate(opts, data)
            elif action == "/update":
                insert = GradeUpdate(opts, data)

        elif ccssType == "/domain":
            if action == "/create":
                insert = DomainCreate(opts, data)
            elif action == "/update":
                insert = DomainUpdate(opts, data)

        elif ccssType == "/cluster":
            if action == "/create":
                insert = ClusterCreate(opts, data)
            elif action == "/update":
                insert = ClusterUpdate(opts, data)

        elif ccssType == "/standard":
            if action == "/create":
                insert = StandardCreate(opts, data)
            elif action == "/update":
                insert = StandardUpdate(opts, data)
            else:
                raise web.NoMethod()

        elif ccssType == "/standard_component":
            if action == "/create":
                insert = ComponentCreate(opts, data)
            elif action == "/update":
                insert = ComponentUpdate(opts, data)

        elif ccssType == "/strand":
            if action == "/create":
                insert = StrandCreate(opts, data)
            elif action == "/update":
                insert = StrandUpdate(opts, data)

        elif ccssType == "/anchor_standard_section":
            if action == "/create":
                insert = SectionCreate(opts, data)
            elif action == "/update":
                insert = SectionUpdate(opts, data)

        elif ccssType == "/anchor_standard":
            if action == "/create":
                insert = AnchorCreate(opts, data)
            elif action == "/update":
                insert = AnchorUpdate(opts, data)

        elif ccssType == "/competency_path":
            web.debug("CreateInsert: Matched on type: %s" % ccssType)
            if action == "/create":
                web.debug("CreateInsert: Matched on action: %s" % action)
                insert = PathCreate(opts, data)
            else:
                raise web.NoMethod()

        elif ccssType == "/learning_resource":
            if action == "/create":
                insert = ResourceCreate(opts, data)
            else:
                raise web.NoMethod()

        elif ccssType == "/competency_container":
            if action == "/create":
                insert = ContainerCreate(opts, data)
            elif action == "/update":
                insert = ContainerUpdate(opts, data)

        elif ccssType == "/competency":
            if action == "/create":
                insert = CompetencyCreate(opts, data)
            elif action == "/update":
                insert = CompetencyUpdate(opts, data)

        elif ccssType == "/strand":
            if action == "/create":
                insert = StrandCreate(opts, data)
            elif action == "/update":
                insert = StrandUpdate(opts, data)

        else:
            raise web.NoMethod()

        web.debug("CreateInsert: insert = %r" % insert)
        return insert

class Insert(object):
    """Base class for inserts"""

    def __init__(self, type, opts, data, httpConfig=None):
        web.debug("Insert.__init__")

        self.type = type
        self.path = "/entity/create"

        self.opts = opts
        if not "access_token" in opts:
            opts["access_token"] = "letmein"
        if not "admin_access_tokens" in opts:
            opts["admin_access_tokens"] = {"letmein":"LRI_ADMIN_USER_0"}

        self.data = data
        self.returnFormat = opts.get("format", "xml")
        self.inserts = []
        self.httpConfig = httpConfig
        if self.httpConfig is None:
            self.httpConfig = httpconfig.HttpConfig(web.ctx.env["DOCUMENT_ROOT"])

    def __repr__(self):
        return "Insert(%s, %r, %r, httpConfig=%r)" % (self.type, 
                                                      self.opts,
                                                      self.data,
                                                      self.httpConfig)

    def __str__(self):
        return """Insert: 
type=%s, 
opts=%r, 
data=%r, 
returnFormat=%s, 
inserts=%r, 
httpConfig=%r,
urls=%r""" % (self.type,
              self.opts,
              self.data,
              self.returnFormat,
              self.inserts,
              self.httpConfig,
              self.getUrls())

    def buildUrn(self, parts):
        parts.insert(0, "urn")
        return ":".join(parts)

    def buildId(self, namespace, uid):
        parts = (namespace, self.type, uid)
        return self.buildUrn(parts)

    def toUrlForm(self, insert):
        decodedOpts = json.dumps(self.opts)
        web.debug("Insert.toUrlForm: decodedOpts = %s" % decodedOpts)

        self.url = "http://%s:%d%s?q=%s&opts=%s" % (self.httpConfig.config["serverhost"], 
                                                    self.httpConfig.config["serverport"], 
                                                    self.path, 
                                                    insert, 
                                                    decodedOpts)
        return self.url

    def getUrls(self):
        """Returns URL that can be sent to LRI server"""

        urls = []
        for insert in self.inserts:
            urls.append(self.toUrlForm(insert))
        return urls

    def getBaseProps(self, soup):
        """Extract common LRI properties from XML"""

        props = {}
        try:
            key = "urn:lri:property_type:contains"
            props["children"] = [x.getText().strip() for x in soup.find(key=key).find_all("value")]
        except AttributeError, e:
            web.debug("Key not found: %s: %r" % (key, e))

        props["creator"] = soup.find(key="urn:lri:property_type:creator").getText().strip()
        props["desc"] = soup.find(key="urn:lri:property_type:description").getText().strip()
        props["id"] = soup.find(key="urn:lri:property_type:id").getText().strip()
        props["name"] = soup.find(key="urn:lri:property_type:name").getText().strip()
        props["uid"] = soup.find(key="uid").getText().strip()

        web.debug("Insert.getBaseProps: base props = %r" % props)

        return props


    def parseXml(self, xml):
        """Parses XML containing new entity"""

        xml = saxutils.unescape(xml)
        soup = BeautifulSoup(xml)
        props = self.getBaseProps(soup)

        return props

    def parseJson(self, decodedJson):
        raise NotImplementedError("Insert.parseJson is not implemented")
        pass

    def buildInserts(self, props):
        """Builds LRI inserts using props from parsed content"""

        query = {}
        if "children" in props:
            query["urn:lri:property_type:contains"] = props["children"]
        query["urn:lri:property_type:creator"] = props["creator"]
        query["urn:lri:property_type:description"] = props["desc"]
        query["urn:lri:property_type:id"] = props["id"]
        query["urn:lri:property_type:name"] = props["name"]
        query["urn:lri:property_type:types"] = ["urn:lri:entity_type:competency", 
                                                "urn:lri:entity_type:learning_objective",
                                                "urn:lri:entity_type:thing"]

        web.debug("Insert.buildInserts: query = %s" % query)

        return query

    def getInserts(self, contentFormat, content):
        """Returns LRI inserts from unparsed content"""

        props = {}
        if contentFormat == "xml":
            props = self.parseXml(content)
        elif contentFormat == "json":
            raise web.BadRequest
        else:
            raise web.BadRequest

        qList = self.buildInserts(props)

        return qList

    def parseOpts(self, opts, key):
        """Extracts key from opts and returns value, modified opts"""

        ID = None
        optsCopy = copy.deepcopy(opts)
        if optsCopy.has_key(key):
            ID = optsCopy[key]
            del(optsCopy[key])

        return ID, optsCopy

class PathCreateOld(Insert):
    def __init__(self, opts, data):
        raise DeprecatedError("PathCreateOld is deprecated")

        Insert.__init__(self, "competency_path", opts, data)
        self.path = "/entity/create"

        self.opts = opts
        if not "access_token" in opts:
            opts["access_token"] = "letmein"
        if not "admin_access_tokens" in opts:
            opts["admin_access_tokens"] = {"letmein":"LRI_ADMIN_USER_0"}

        self.data = data
        self.returnFormat = opts.get("format", "xml")
        self.inserts = self.getInserts(self.returnFormat, self.data)

        web.debug(repr(self))
        web.debug(str(self))
        web.debug("PathCreateOld.__init__: urls = %r" % self.getUrls())

    def parseXml(self, xml):
        raise DeprecatedError("PathCreateOld is deprecated")

        xml = saxutils.unescape(xml)
        soup = BeautifulSoup(xml)
        path_id = soup.find(key="urn:lri:property_type:id").getText().strip()
        path_name = soup.find(key="urn:lri:property_type:name").getText().strip()
        path_desc = soup.find(key="urn:lri:property_type:description").getText().strip()
        author_id = soup.find(key="urn:lri:property_type:authored_by").getText().strip()
        competency_list = [x.getText().strip() for x in soup.find(key="urn:lri:property_type:path_step").find_all("value")]

        print("\nparse_path_xml: path_id = %s" % path_id)
        print("parse_path_xml: path_name = %s" % path_name)
        print("parse_path_xml: path_description = %s" % path_desc)
        print("parse_path_xml: author_id = %s" % author_id)
        print("parse_path_xml: competency_list = %r" % competency_list)

        return path_id, path_name, path_desc, author_id, competency_list

    def parseJson(self, decodedJson):
        """Extracts keys from json doc. Expected format:
{
  "urn:lri:property_type:id": path_id,
  "urn:lri:property_type:name": path_name,
  "urn:lri:property_type:description": path_description,
  "urn:lri:property_type:authored_by": author_id,
  "urn:lri:property_type:path_step": [
    competency_id_1,
    competency_id_2,
    ...
    competency_id_n
  ]
}
"""

        raise DeprecatedError("PathCrateOld is deprecated")

        json_decoded = decodedJson

        path_id = json_decoded["urn:lri:property_type:id"]
        path_name = json_decoded["urn:lri:property_type:name"]
        path_desc = json_decoded["urn:lri:property_type:description"]
        author_id = json_decoded["urn:lri:property_type:authored_by"]
        competency_list = json_decoded["urn:lri:property_type:path_step"]

        return path_id, path_name, path_desc, author_id, competency_list

    def buildInserts(self, pathId, pathName, pathDesc, authorId, competencyList):
        """Constructs queries that save a competency_path"""

        raise DeprecatedError("PathCreateOld is deprecated")

        path_id = pathId
        path_name = pathName
        path_description = pathDesc
        author_id = authorId
        competency_list = competencyList

        print("\nbuild_path_query: path_id = %s" % path_id)
        print("build_path_query: path_name = %s" % path_name)
        print("build_path_query: path_description = %s" % path_description)
        print("build_path_query: author_id = %s" % author_id)
        print("build_path_query: competency_list = %r" % competency_list)

        # Query to create competency_path
        path_query = {}
        path_query["urn:lri:property_type:id"] = path_id
        path_query["urn:lri:property_type:name"] = path_name
        path_query["urn:lri:property_type:description"] = path_description
        path_query["urn:lri:property_type:authored_by"] = author_id
        path_query["urn:lri:property_type:types"] = ["urn:lri:entity_type:thing",
                                                       "urn:lri:entity_type:competency",
                                                       "urn:lri:entity_type:competency_path"]

        # path id         = urn:ccss:ordering:path1
        # competency id   = urn:ccss:grade_levelLmath:K
        # step_id         = urn:ccss:step:ordering:path1-grade_level:math:K
        # common          = urn:ccss
        # path id rest    = ordering:path1
        # competency rest = grade_level:math:K
        # step_id         = root + : + step + : + path_id_rest + - + competency_id_rest

        # Queries to create path_steps
        count = 1
        seen = []
        step_list = []
        step_queries = []
        step_id_basename = os.path.basename(path_id)
        step_name_basename = os.path.basename(path_name)
        path_id_namespace = os.path.dirname(path_id)
        previous = None
        for competency in competency_list:
            print("\nbuild_save_path_query:   competency = %s" % competency)

            step_query = {}

            print("build_save_path_query:   path_id = %s" % path_id)

            common = os.path.commonprefix([path_id, competency])
            print("build_save_path_query:   common = %s" % common)

            root = common
            print("build_save_path_query:   root = %s" % root)

            competency_parts = competency.split(root)
            print("build_save_path_query:   competency_parts = %r" % competency_parts)

            path_parts = path_id.split(root)
            print("build_save_path_query:   path_parts = %r" % path_parts)

            step_id = "%sstep:%s-%s" % (root, path_parts[1], competency_parts[1])
            print("build_save_path_query:   step_id = %s" % step_id)
            
            step_name = os.path.basename(competency) #"%s_%s" % (step_id_basename, step_name_basename)
            if competency in seen:
                step_id = "%s-%d" % (step_id, count)
                step_name = "%s-%d" % (step_name, count)
                print("build_save_path_query:     step_id = %s" % step_id)
                print("build_save_path_query:     step_name = %s" % step_name)
                count += 1

            step_query["urn:lri:property_type:id"] = step_id
            step_query["urn:lri:property_type:name"] = step_name
            step_query["urn:lri:property_type:types"] = ["urn:lri:entity_type:thing",
                                                           "urn:lri:entity_type:path_step"]
            step_query["urn:lri:property_type:competency_in_path"] = competency

            if previous != None:
                step_query["urn:lri:property_type:previous"] = previous
            previous = step_id

            step_queries.append(step_query)

            step_list.append(step_id)

            seen.append(competency)

        print("build_save_path_query: step_list: ")
        for step in step_list:
            print(step)

        print("build_save_path_query: step_queries: ")
        for query in step_queries:
            action = "/entity/create"
            print(action)
            print(query)

        # First create path_steps
        queries = step_queries

        # Finish path_query and add to list
        path_query["urn:lri:property_type:path_step"] = step_list
        queries.append(path_query)

        # Convert to json
        json_queries = []
        for query in queries:
            json_queries.append(json.dumps(query))

        return json_queries

    def getInserts(self, contentFormat, content):
        """Returns a list of lri queries that save a competency_path"""

        raise DeprecatedError("PathCreateOld is deprecated")

        content_format = contentFormat

        self.path = "/entity/create"

        path_id = path_name = path_desc = ""
        author_id = ""
        competency_list = []
        if content_format == "xml":
            path_id, path_name, path_desc, author_id, competency_list = self.parseXml(content)
        elif content_format == "json":
            path_id, path_name, path_desc, author_id, competency_list = self.parseJson(content)
        else:
            raise web.BadRequest

        q_list = self.buildInserts(path_id, path_name, path_desc, author_id, competency_list)

        print("get_save_path_queries: self.path = %s" % self.path)
        print("get_save_path_queries: q_list (len=%d): " % len(q_list))
        for q in q_list:
            print("get_save_path_queries:   q = %r" % q)

        #return [{}]
        return q_list

class Step(Insert):
    """Step w/single competency"""
    pass

class Step(Insert):
    """Step w/1 or more competencies"""
    def __init__(self, competencyList):
        self.query = {}

class OrderingStep(Insert):
    """Step that wraps a path"""
    def __init__(self, stepList):
        self.query = {}

class PathCreate(Insert):
    """For creating competency_path"""

    def __init__(self, opts, data):
        web.debug("PathCreate.__init__")

        Insert.__init__(self, "competency_path", opts, data)
        self.path = "/entity/create"

        self.opts = opts
        if not "access_token" in opts:
            opts["access_token"] = "letmein"
        if not "admin_access_tokens" in opts:
            opts["admin_access_tokens"] = {"letmein":"LRI_ADMIN_USER_0"}

        # For making unique ids
        self.randStr = self.makeRandom()
        web.debug("PathCreate.__init__: self.randStr = %s" % self.randStr)
        self.seenIds = []

        self.data = data
        self.returnFormat = opts.get("format", "xml")
        self.inserts = self.getInserts(self.returnFormat, self.data)

        web.debug(repr(self))
        web.debug(str(self))
        web.debug("PathCreate.__init__: urls = %r" % self.getUrls())

    def parseXml(self, xml):
        """Extracts LRI properties from xml"""

        thisName = "parseXml"
        web.debug(thisName + ": xml = %s" % xml)

        xml = saxutils.unescape(xml)
        web.debug(thisName + ": unescaped xml = %s" % xml)

        soup = BeautifulSoup(xml)
        web.debug(thisName + ": soup = %s" % soup)

        pathId = None
        tmp = soup.find(key="urn:lri:property_type:id")
        if tmp:
            pathId = tmp.getText().strip()

        pathName = None
        tmp = soup.find(key="urn:lri:property_type:name")
        if tmp:
            pathName = tmp.getText().strip()

        pathDesc = None
        tmp = soup.find(key="urn:lri:property_type:description")
        if tmp:
            pathDesc = tmp.getText().strip()

        authorName = None
        tmp = soup.find(key="urn:lri:property_type:authored_by")
        if tmp:
            authorName = tmp.getText().strip()
    
        pathSteps = None
        tmp = soup.find(key="urn:lri:property_type:path_step")
        if tmp:
            pathSteps = tmp
        web.debug(thisName + ": pathSteps: ")
        web.debug(pathSteps)

        return pathId, pathName, pathDesc, authorName, pathSteps

    def parseJson(self, decodedJson):
        return None, None, None, None, []

    def makeRandom(self):
        """Makes a random LRI id"""

        thisName = "makeRandom"

        r = str(random.random()).split(".")[1]
        web.debug(thisName + ": r = %s" % r)

        return r

    def makePath(self, props={}):
        """Makes a path"""

        thisName = "makePath"
        web.debug(thisName + ": props = %r" % props)

        query = {}
        if len(props) > 0:
            for prop in props:
                query[prop] = props[prop]
        else:
            id = makeId("container")
            query["urn:lri:property_type:id"] = id
            query["urn:lri:property_type:name"] = self.makeName("container", id)

        query["urn:lri:property_type:types"]= ["urn:lri:entity_type:thing",
                                               "urn:lri:entity_type:competency",
                                               "urn:lri:entity_type:competency_path"]

        query["urn:lri:property_type:path_step"] = []

        web.debug(thisName + ": query: ")
        web.debug(query)

        return query          

    def makeId(self, type, ns="lrihelper", commonName="lrihelper"):
        """Makes a path or path_step id"""

        thisName = "makeId"
        web.debug(thisName + ": type       = %s" % type)
        web.debug(thisName + ": ns         = %s" % ns)
        web.debug(thisName + ": commonName = %s" % commonName)

        id = "urn:"
        id += ns + ":"
        id += type + ":"
        id += commonName + "-"

        id += self.randStr

        if id in self.seenIds:
            id += "-" + str(len(self.seenIds) + 1)
        self.seenIds.append(id)

        web.debug(thisName + ": id = %s" % id)

        return id

    def makeName(self, type, id):
        """Makes a path or path_step name"""

        thisName = "makeName"
        web.debug(thisName + ": type = %s, id = %s" % (type, id))

        parts = id.split(":")
        name = " ".join(parts[1:])

        web.debug(thisName + ": name = %s" % name)

        return name

    def makeContainer(self, competencyList):
        """Makes a container to hold given competencies

Allows for multiple competencies per step

"""
        thisName = "makeContainer"

        query = {}
        id = self.makeId("container")
        query["urn:lri:property_type:id"] = id
        query["urn:lri:property_type:name"] = self.makeName("container", id)
        query["urn:lri:property_type:types"] = ["urn:lri:entity_type:thing",
                                                "urn:lri:entity_type:competency",
                                                "urn:lri:entity_type:competency_container"]
        query["urn:lri:property_type:contains"] = competencyList

        web.debug(thisName + ": id = %s" % id)

        web.debug(thisName + ": query: ")
        web.debug(query)

        return query

    def makeStep(self, xml):
        """Makes path_steps from xml"""

        thisName = "makeStep"
        web.debug(thisName + ": xml = %s" % xml)

        pairs = xml.findAll("pair")
        stepType = pairs[0].value.getText().strip()

        competencyList = []
        index = len(pairs) - 1
        for value in pairs[index].findAll("value"):
            competencyList.append(value.getText().strip())

        previous = None
        tmp = xml.find(key="previous")
        if tmp:
            previous = tmp.getText().strip()

        orderId = None
        tmp = xml.find(key="orderId")
        if tmp:
            orderId = tmp.getText().strip()

        web.debug(thisName + ": stepType = %r" % stepType)
        web.debug(thisName + ": competencyList: ")
        web.debug(competencyList)
        web.debug(thisName + ": previous = %r" % previous)
        web.debug(thisName + ": orderId = %r" % orderId)

        stepQuery = {}
        stepId = self.makeId("step")
        stepQuery["urn:lri:property_type:id"] = stepId
        stepQuery["urn:lri:property_type:name"] = self.makeName("step", stepId)

        if previous:
            stepQuery["previous"] = previous

        stepQuery["orderId"] = orderId

        containerQuery = self.makeContainer(competencyList)
        stepQuery["urn:lri:property_type:competency_in_path"] = containerQuery["urn:lri:property_type:id"]

        stepQuery["urn:lri:property_type:types"] = ["urn:lri:entity_type:thing",
                                                "urn:lri:entity_type:path_step"]

        # XXX: RESUME HERE
        web.debug(thisName + ": stepQuery: ")
        web.debug(stepQuery)
        web.debug(thisName + ": containerQuery: ")
        web.debug(containerQuery)

        return stepQuery, containerQuery

    def makeOrderingStep(self, xml):
        """Makes an ordering path_step

Used to order steps in path

"""

        thisName = "makeOrderingStep"

        pairs = xml.findAll("pair")
        stepType = pairs[0].value.getText().strip()
        orderId = pairs[1].value.getText().strip()

        web.debug(thisName + ": Creating path")
        pathQuery = self.makePath({})

        pathSteps = xml.find(key="urn:lri:property_type:path_step")

        stepList = []
        stepQueries = []
        containerQueries = []
        for step in pathSteps.findAll("value"):
            if step.pair:
                stepQuery = {}
                if step.pair["key"] == "type":
                    val = step.pair.value.getText()
                    if val == "step":
                        web.debug(thisName + ": Creating step")
                        stepQuery, containerQuery = self.makeStep(step)
                        stepQueries.append(stepQuery)
                        containerQueries.append(containerQuery)
                        stepList.append(stepQuery["urn:lri:property_type:id"])

        pathQuery["urn:lri:property_type:path_step"] = stepList
        pathQuery["orderId"] = orderId

        return pathQuery, stepQueries, containerQueries

    def buildInserts(self, pathId, pathName, pathDesc, authorName, pathSteps):
        """Builds LRI inserts

NOTE: authorName must be LRI id

"""

        thisName = "buildInserts"
        web.debug(thisName + ": pathId     = %s" % pathId)
        web.debug(thisName + ": pathName   = %s" % pathName)
        web.debug(thisName + ": pathDesc   = %s" % pathDesc)
        web.debug(thisName + ": authorName = %s" % authorName)
        web.debug(thisName + ": pathSteps  = %r" % pathSteps)

        # Create path
        props = {
            "urn:lri:property_type:id": pathId,
            "urn:lri:property_type:name": pathName,
            "urn:lri:property_type:description": pathDesc,
            "urn:lri:property_type:authored_by": authorName,
            }
        web.debug(thisName + ": props = %r" % props)
        pathQuery = self.makePath(props)

        # Create steps
        stepList = []
        seenSteps = []
        queries = []
        web.debug(thisName + ": Creating steps: ")
        for step in pathSteps.findAll("value"):
            if step.pair:
                stepQuery = {}
                orderingQueries = []
                if step.pair["key"] == "type":
                    stepType = step.pair.value.getText()
                    if stepType == "step":
                        stepOrderId = step.findNext("pair").findNext("pair").value.getText()
                        if not stepOrderId in seenSteps:
                            # Skip steps makeOrderingStep creates
                            web.debug(thisName + ": Creating step")
                            web.debug(step)
                            stepQuery, containerQuery = self.makeStep(step)
                            queries.append(containerQuery)
                            queries.append(stepQuery)
                            stepList.append(stepQuery["urn:lri:property_type:id"])
                            seenSteps.append(stepQuery["orderId"])
                    elif stepType == "ordering":
                        web.debug(thisName + ": Creating ordering step")
                        pathQuery, stepQueries, containerQueries = self.makeOrderingStep(step)
                        for stepQuery in stepQueries:
                            seenSteps.append(stepQuery["orderId"])
                        queries += containerQueries
                        queries += stepQueries
                        queries.append(pathQuery)
                        stepList.append(pathQuery["urn:lri:property_type:id"])
                                    
        # Order steps
        for query in queries:
            if "urn:lri:entity_type:path_step" not in query["urn:lri:property_type:types"]:
                continue

            if "previous" not in query:
                continue

            previous = query["previous"]
            for q in queries:
                if "urn:lri:entity_type:path_step" not in q["urn:lri:property_type:types"]:
                    continue

                if query == q:
                    # Skip this
                    continue

                if "orderId" not in q:
                    # Skip containers
                    continue

                try:
                    orderId = q["orderId"]
                    if orderId == previous:
                        id = q["urn:lri:property_type:id"]
                        query["urn:lri:property_type:previous"] = id
                except KeyError, e:
                    web.debug("KeyError: q: %r" % q)
                    raise e

        # Remove tmp keys previous and orderId
        for query in queries:
            if "previous" in query:
                del query["previous"]

            if "orderId" in query:
                del query["orderId"]

        pathQuery["urn:lri:property_type:path_step"] = []
        for step in stepList:
            if step.find("step") != -1:
                pathQuery["urn:lri:property_type:path_step"].append(step)
        queries.append(pathQuery)

        # Convert query to json before sending to LRI server
        jsonQueries = []
        for query in queries:
            jsonQueries.append(json.dumps(query))

        return jsonQueries

    def getInserts(self, contentFormat, content):
        """Returns list of LRI inserts to insert given content in LRI"""

        thisName = "getInserts"
        web.debug(thisName + ": contentFormat = %s" % contentFormat)
        web.debug(thisName + ": content = %s" % content)

        self.path = "/entity/create"

        if contentFormat == "xml":
            pathId, pathName, pathDesc, authorName, pathSteps = self.parseXml(content)
        elif contentFormat == "json":
            raise web.BadRequest
        else:
            raise web.BadRequest

        queries = self.buildInserts(pathId, pathName, pathDesc, authorName, pathSteps)

        print
        web.debug(thisName + ": queries: ")
        for query in queries:
            print query

        #return [{}]
        return queries

# Path w/multiple competency_in_path in step
class MultiCompetencyStepPath(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("MultiCompetencyStepPath is not implemented")

        Insert.__init__(self, "MultiCompetencyStepPath", opts, data)
        self.inserts = self.getInserts(self.returnFormat, self.data)
        print(repr(self))
        print(str(self))
        web.debug("MultiCompetencyStepPathCreate.__init__: urls = %r" % self.getUrls())

    def parseXml(self, xml):
        pass

    def buildInserts(self, props):
        pass

    def getInserts(self, contentFormat, content):
        pass

# Non-linear path
class NonLinearPath(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("NonLinearPath is not implemented")

        Insert.__init__(self, "NonLinearPath", opts, data)
        self.inserts = self.getInserts(self.returnFormat, self.data)
        print(repr(self))
        print(str(self))
        web.debug("NonLinearPathCreate.__init__: urls = %r" % self.getUrls())

    def parseXml(self, xml):
        pass

    def buildInserts(self, props):
        pass

    def getInserts(self, contentFormat, content):
        pass

class ResourceCreate(Insert):
    """For creating learning_resources"""

    def __init__(self, opts, data):
        Insert.__init__(self, "learning_resource", opts, data)
        self.path = "/entity/create"
        self.opts = opts
        self.data = data
        self.returnFormat = opts.get("format", "xml")
        self.inserts = self.getInserts(self.returnFormat, self.data)

    def parseXml(self, xml):
        """Extracts keys from XML doc. Expected format:

<xml>
  <pair key='urn:lri:property_type:id'>
    <value>resource_id</value>
  </pair>
  <pair key='urn:lri:property_type:name'>
    <value>resource_name</value>
  </pair>
  <pair key='urn:lri:property_type:description'>
    <value>resource_description</value>
  </pair>
  <pair key='urn:lri:property_type:teaches'>
    <value>competency_1_id</value>
    <value>competency_2_id</value>
    ...
    <value>competency_n_id</value>
  </pair>
</xml>

"""

        xml = saxutils.unescape(xml)
        soup = BeautifulSoup(xml)
        resource_id = soup.find(key="urn:lri:property_type:id").getText().strip()
        resource_name = soup.find(key="urn:lri:property_type:name").getText().strip()
        resource_desc = soup.find(key="urn:lri:property_type:description").getText().strip()
        competency_list = [x.getText().strip() for x in soup.find(key="urn:lri:property_type:teaches").find_all("value")]

        return resource_id, resource_name, resource_desc, competency_list

    def parseJson(self, decodedJson):
        """Extracts keys from json doc. Expected format:
{
  "urn:lri:property_type:id": resource_id,
  "urn:lri:property_type:name": resource_name,
  "urn:lri:property_type:description": resource_description,
  "urn:lri:property_type:teaches": [
    competency_id_1,
    competency_id_2,
    ...
    competency_id_n
  ]
}
"""

        json_decoded = decodedJson

        resource_id = json_decoded["urn:lri:property_type:id"]
        resource_name = json_decoded["urn:lri:property_type:name"]
        resource_desc = json_decoded["urn:lri:property_type:description"]
        competency_list = json_decoded["urn:lri:property_type:teaches"]

        return path_id, path_name, path_desc, author_id, competency_list

    def buildInserts(self, resourceId, resourceName, resourceDesc, competencyList):
        """Constructs queries that save a learning_resource"""

        resource_id = resourceId
        resource_name = resourceName
        resource_desc = resourceDesc
        competency_list = competencyList

        # Query to create learning_resource
        resource_query = {}
        resource_query["urn:lri:property_type:id"] = resource_id
        resource_query["urn:lri:property_type:name"] = resource_name
        resource_query["urn:lri:property_type:description"] = resource_desc
        resource_query["urn:lri:property_type:types"] = ["urn:lri:entity_type:thing",
                                                           "urn:lri:entity_type:learning_resource"]
        resource_query["urn:lri:property_type:teaches"] = competency_list

        # Convert to json
        json_query = json.dumps(resource_query)
        print("\n\n\nResourceCreate.buildInserts: json_query=%r\n\n\n" % json_query)

        return [json_query]

    def getInserts(self, contentFormat, content):
        """Returns a list of lri queries that saves a learning_resource"""

        content_format = contentFormat

        self.path = "/entity/create"

        resource_id = resource_name = resource_desc = ""
        competency_list = []
        if content_format == "xml":
            resource_id, resource_name, resource_desc, competency_list = self.parseXml(content)
        elif content_format == "json":
            resource_id, resource_name, resource_desc, competency_list = self.parseJson(content)

        q_list = self.buildInserts(resource_id, resource_name, resource_desc, competency_list)

        print("ResourceCreate.getInserts: self.path = %s" % self.path)
        print("ResourceCreate.getInserts: self.q_list (len=%d): " % len(q_list))
        for q in q_list:
            print("ResourceCreate.getInserts:   q = %r" % q)

        #return [{}]
        return q_list

class InitiativeCreate(Insert):
    """Creates an initiative"""

    def __init__(self, opts, data):
        Insert.__init__(self, "initiative", opts, data)
        self.inserts = self.getInserts(self.returnFormat, self.data)
        print(repr(self))
        print(str(self))
        web.debug("InitiativeCreate.__init__: urls = %r" % self.getUrls())
       
    def parseXml(self, xml):
        """Parses xml"""

        props = Insert.parseXml(self, xml)
        return props

    def buildInserts(self, props):
        """Builds LRI inserts"""

        query = Insert.buildInserts(self, props)

        query["urn:lri:property_type:types"].append("urn:ccss:entity_type:competency_container")
        query["urn:lri:property_type:types"].append("urn:ccss:entity_type:initiative")

        # Convert to json
        jsonQuery = json.dumps(query)
        print("\n\n\nInitiativeCreate.buildInserts: jsonQuery=%r\n\n\n" % jsonQuery)

        return [jsonQuery]

    def getInserts(self, contentFormat, content):
        """Returns list of LRI inserts"""

        qList = Insert.getInserts(self, contentFormat, content)

        print("InitiativeCreate.getInserts: self.path = %s" % self.path)
        print("InitiativeCreate.: qList (len=%d): " % len(qList))
        for q in qList:
            print("InitiativeCreate.:   q = %r" % q)

        return qList

class FrameworkCreate(Insert):
    """Creates a framework"""

    def __init__(self, opts, data):
        Insert.__init__(self, "framework", opts, data)
        self.inserts = self.getInserts(self.returnFormat, self.data)
        print(repr(self))
        print(str(self))
        web.debug("FrameworkCreate.__init__: urls = %r" % self.getUrls())
       
    def parseXml(self, xml):
        """Parses XML"""

        props = Insert.parseXml(self, xml)

        xml = saxutils.unescape(xml)
        soup = BeautifulSoup(xml)
        try:
            key = "urn:lri:property_type:contained_by"
            props["parent"] = soup.find(key=key).getText().strip()
        except AttributeError, e:
            web.debug("Key not found: %s: %r" % (key, e))

        return props

    def buildInserts(self, props):
        """Builds LRI inserts"""

        query = Insert.buildInserts(self, props)

        if "parent" in props:
            query["urn:lri:property_type:contained_by"] = props["parent"]
        query["urn:lri:property_type:types"].append("urn:ccss:entity_type:competency_container")
        query["urn:lri:property_type:types"].append("urn:ccss:entity_type:framework")

        # Convert to json
        jsonQuery = json.dumps(query)
        print("\n\n\nFrameworkCreate.buildInserts: jsonQuery=%r\n\n\n" % jsonQuery)

        return [jsonQuery]

    def getInserts(self, contentFormat, content): 
        """Returns list of LRI inserts"""

        qList = Insert.getInserts(self, contentFormat, content)

        print("FrameworkCreate.getInserts: self.path = %s" % self.path)
        print("FrameworkCreate.: queries (len=%d): " % len(qList))
        for q in qList:
            print("FrameworkCreate.:   query = %r" % q)

        return qList

class SetCreate(Insert):
    """Creates a set"""

    def __init__(self, opts, data):
        Insert.__init__(self, "set", opts, data)
        self.inserts = self.getInserts(self.returnFormat, self.data)
        print(repr(self))
        print(str(self))
        web.debug("SetCreate.__init__: urls = %r" % self.getUrls())
       
    def parseXml(self, xml):
        """Parses XML"""

        props = Insert.parseXml(self, xml)

        xml = saxutils.unescape(xml)
        soup = BeautifulSoup(xml)
        try:
            key = "urn:lri:property_type:contained_by"
            props["parent"] = soup.find(key=key).getText().strip()
        except AttributeError, e:
            web.debug("Key not found: %s: %r" % (key, e))

        return props

    def buildInserts(self, props):
        """Builds LRI inserts"""

        query = Insert.buildInserts(self, props)

        if "parent" in props:
            query["urn:lri:property_type:contained_by"] = props["parent"]
        query["urn:lri:property_type:types"].append("urn:ccss:entity_type:competency_container")
        query["urn:lri:property_type:types"].append("urn:ccss:entity_type:set")

        # Convert to json
        jsonQuery = json.dumps(query)
        print("\n\n\nSetCreate.buildInserts: jsonQuery=%r\n\n\n" % jsonQuery)

        return [jsonQuery]

    def getInserts(self, contentFormat, content): 
        """Returns list of LRI inserts"""

        qList = Insert.getInserts(self, contentFormat, content)

        print("SetCreate.getInserts: self.path = %s" % self.path)
        print("SetCreate.: qList (len=%d): " % len(qList))
        for q in qList:
            print("SetCreate.:   q = %r" % q)

        return qList

class GradeCreate(Insert):
    """Creates a grade_level"""

    def __init__(self, opts, data):
        Insert.__init__(self, "grade_level", opts, data)
        self.inserts = self.getInserts(self.returnFormat, self.data)
        print(repr(self))
        print(str(self))
        web.debug("GradeCreate.__init__: urls = %r" % self.getUrls())
       
    def parseXml(self, xml):
        """Parses XML"""

        web.debug("GradeCreate.parseXml")

        xml = saxutils.unescape(xml)
        soup = BeautifulSoup(xml)
        grades = soup.find_all(key="grade_level")
        propsList = []
        prevGradeId = ""
        for grade in grades:
            props = self.getBaseProps(grade)

            if prevGradeId:
                props["previous"] = prevGradeId
            try:
                key = "urn:lri:property_type:contained_by"
                props["parent"] = soup.find(key=key).getText().strip()
            except AttributeError, e:
                web.debug("Key not found: %s: %r" % (key, e))

            propsList.append(props)

            prevGradeId = props["id"]

            web.debug("GradeCreate.parseXml:    props: ")
            for prop in props:
                web.debug("GradeCreate.parseXml:       %s : %s" % (prop, props[prop]))
        return propsList

    def buildInserts(self, propsList):
        """Builds LRI inserts"""

        web.debug("GradeCreate.buildInserts")

        jsonQueries = []
        for props in propsList:
            query = Insert.buildInserts(self, props)

            if "previous" in props:
                query["urn:lri:property_type:previous"] = props["previous"]

            if "parent" in props:
                query["urn:lri:property_type:contained_by"] = props["parent"]
            query["urn:lri:property_type:types"].append("urn:ccss:entity_type:competency_container")
            query["urn:lri:property_type:types"].append("urn:ccss:entity_type:grade_level")

            # Convert to json
            jsonQuery = json.dumps(query)
            print("\n\n\nGradeCreate.buildInserts: jsonQuery=%r\n\n\n" % jsonQuery)
            jsonQueries.append(jsonQuery)

        return jsonQueries

    def getInserts(self, contentFormat, content): 
        """Returns list of LRI inserts"""

        web.debug("GradeCreate.getInserts")

        qList = Insert.getInserts(self, contentFormat, content)

        print("GradeCreate.getInserts: self.path = %s" % self.path)
        print("GradeCreate.getInserts: qList (len=%d): " % len(qList))
        for q in qList:
            print("GradeCreate.:   q = %r" % q)

        return qList

class DomainCreate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("DomainCreate is not implemented")
       
class ClusterCreate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("ClusterCreate is not implemented")

class StandardCreate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("StandardCreate is not implemented")

class ComponentCreate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("ComponentCreate is not implemented")

class StrandCreate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("StrandCreate is not implemented")

class SectionCreate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("SectionCreate is not implemented")

class AnchorCreate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("AnchorCreate is not implemented")

class CompetencyCreate(Insert):
    """/ccss/competency/create

Creates a competency

"""

    def __init__(self, opts, data):
        Insert.__init__(self, "competency", opts, data)
        self.inserts = self.getInserts(self.returnFormat, self.data)
        print(repr(self))
        print(str(self))
        web.debug("CompetencyCreate.__init__: urls = %r" % self.getUrls())
       
    def parseXml(self, xml):
        """Parse XML"""

        props = Insert.parseXml(self, xml)

        xml = saxutils.unescape(xml)
        soup = BeautifulSoup(xml)
        try:
            key = "urn:lri:property_type:contained_by"
            props["parent"] = soup.find(key=key).getText().strip()
        except AttributeError, e:
            web.debug("Key not found: %s: %r" % (key, e))

        try:
            key = "urn:lri:property_type:completion_criterion"
            props["completion_criterion"] = soup.find(key=key).getText().strip()
        except AttributeError, e:
            web.debug("Key not found: %s: %r" % (key, e))

        return props

    def parseJson(self, decodedJson):
        """ TODO """
        pass


    def buildInserts(self, props):
        """Builds LRI inserts"""

        query = Insert.buildInserts(self, props)

        if "parent" in props:
            query["urn:lri:property_type:contained_by"] = props["parent"]

        if "completion_criterion" in props:
            query["urn:lri:property_type:completion_criterion"] = props["completion_criterion"]
        query["urn:lri:property_type:types"].append("urn:lri:entity_type:competency")

        jsonQuery = json.dumps(query)
        print("\n\n\nCompetencyCreate.buildInserts: jsonQuery=%r\n\n\n" % jsonQuery)

        return [jsonQuery]

    def getInserts(self, contentFormat, content):
        """Returns list of LRI inserts"""

        qList = Insert.getInserts(self, contentFormat, content)

        web.debug("CompetencyCreate: getInserts: queries: ")
        for q in qList:
            web.debug("CompetencyCreate: getInserts:   query = %s" % q)

        return qList

class ContainerCreate(Insert):
    """Creates a competency_container"""

    def __init__(self, opts, data):
        Insert.__init__(self, "competency_container", opts, data)
        self.inserts = self.getInserts(self.returnFormat, self.data)
        print(repr(self))
        print(str(self))
        web.debug("ContainerCreate.__init__: urls = %r" % self.getUrls())
       
    def parseXml(self, xml):
        """Parses XML"""

        props = Insert.parseXml(self, xml)

        xml = saxutils.unescape(xml)
        soup = BeautifulSoup(xml) 
        try:
            key = "urn:lri:property_type:contained_by"
            props["parent"] = soup.find(key=key).getText().strip()
        except AttributeError, e:
            web.debug("Key not found: %s: %r" % (key, e))

        try:
            key = "urn:lri:property_type:completion_criterion"
            props["completion_criterion"] = soup.find(key=key).getText().strip()
        except AttributeError, e:
            web.debug("Key not found: %s: %r" % (key, e))

        return props

    def parseJson(self, decodedJson):
        """ TODO """
        pass

    def buildInserts(self, props):
        """Builds LRI inserts"""

        query = Insert.buildInserts(self, props)

        if "parent" in props:
            query["urn:lri:property_type:contained_by"] = props["parent"]

        if "completion_criterion" in props:
            query["urn:lri:property_type:completion_criterion"] = props["completion_criterion"]
        query["urn:lri:property_type:types"].append("urn:lri:entity_type:competency_container")

        jsonQuery = json.dumps(query)
        print("\n\n\nContainerCreate.buildInserts: jsonQuery=%r\n\n\n" % jsonQuery)

        return [jsonQuery]

    def getInserts(self, contentFormat, content):
        """Returns list of LRI inserts"""

        qList = Insert.getInserts(self, contentFormat, content)

        web.debug("ContainerCreate: getInserts: queries: ")
        for q in qList:
            web.debug("ContainerCreate: getInserts:   query = %s" % q)

        return qList


##### Update #####

# Generic routines independent of CCSS or LRI type
def parseXml(xml):
    """Parses XML"""

    web.debug("parseXml")

    xml = saxutils.unescape(xml)
    soup = BeautifulSoup(xml)
    id = soup.find(key='urn:lri:property_type:id').getText().strip()
    web.debug("parseXml: id = %s" % id)

    updates = soup.find(key='updates')
    web.debug("parseXml: updates = %r" % updates)

    props = soup.find_all(key='property')
    web.debug("parseXml: props = %r" % props)

    updates = []
    for prop in props:
        web.debug("parseXml:    prop = %r" % prop)

        all = prop.findAll()
        web.debug("parseXml:    all = %r" % all)

        property = all[0].getText()
        web.debug("parseXml:    property = %s" % property)

        value = all[1].getText()
        web.debug("parseXml:    value = %s" % value)

        updates.append((id, property, value))

    return updates

def get(path, query, opts):
    """Does a GET"""

    web.debug("get")

    httpConfig = httpconfig.HttpConfig(web.ctx.env["DOCUMENT_ROOT"])
    url = "http://%s:%d/%s?q=%s&opts=%s" % (httpConfig.config["serverhost"], 
                                            httpConfig.config["serverport"], 
                                            path, 
                                            query, 
                                            opts)
    response = requests.get(url)
    web.debug("get: url = %s" % url)
    web.debug("get: status = %s" % response.status_code)

    return response

def updateProperty(guid, value, opts):
    """Updates an existing LRI property

* guid: LRI property GUID
* value: New value

"""

    web.debug("updateProperty")

    path = "/property/update"
    query = '{"guid":"%s","value":"%s"}' % (guid, value)
    web.debug("updateProperty: ", path, query, opts)
    response = get(path, query, opts)

    return response

def createProperty(iguid, property, value, opts):
    """Creates a new LRI property

* iguid: LRI entity GUID
* property: LRI property name
* value: New value

"""
    web.debug("createProperty")

    path = "/property/create"
    query = '{"from":"%s","%s":"%s"}' % (iguid, property, value)
    web.debug("createProperty: ", path, query, opts)
    response = get(path, query, opts)

    return response

def runUpdates(updates, opts):
    """Run list of LRI updates"""

    web.debug("runUpdates")

    path = "/entity/search"
    if not "details" in opts:
        opts["details"] = True
    if not "access_token" in opts:
        opts["access_token"] = "letmein"
    if not "admin_access_tokens" in opts:
        opts["admin_access_tokens"] = {"letmein":"LRI_ADMIN_USER_0"}
    opts = json.dumps(opts)

    responses = []
    web.debug("runUpdates: %d updates" % len(updates))
    for update in updates:
        web.debug(" ===== update %d ===== " % updates.index(update))

        id, property, value = update
        web.debug("runUpdates:    %s, %s, %s" %( id, property, value))

        # Get guid of property
        query = '{"urn:lri:property_type:id":"%s"}' % id
        response = get(path, query, opts)
        web.debug("runUpdates:    status = %s" % response.json["status"])
        if "message" in response.json:
            web.debug("runUpdates:    message = %s" % response.json["message"])

        guid = ""
        iguid = ""
        web.debug("runUpdates:    response.json = %r" % response.json)
        for r in response.json["response"]:
            web.debug("runUpdates:       in response")

            props = r["props"]
            for prop in props:
                web.debug("runUpdates:          in props")

                if len(iguid) == 0:
                    iguid = props["urn:lri:property_type:guid"]
                    web.debug("runUpdates:    iguid = %s" % iguid)

                web.debug("runUpdates:          prop = %s" % prop)
                web.debug("runUpdates:          property = %s" % property)
                if prop == property:
                    for key in props[prop]:
                        web.debug("runUpdates:             key = %s" % key)
                        vals = props[prop][key]
                        for val in vals:
                            web.debug("runUpdates:                val = %s" % val)
                            guid = val["guid"]
                            web.debug("runUpdates:                guid = %s" % guid)

        if guid == "":
            # Property doesn't exist
            # Create it
            response = createProperty(iguid, property, value, opts)
            responses.append(response)
        else:
            # Property exists
            # Update it
            web.debug("runUpdates: guid=%s, value=%s, opts=%r" % (guid, value, opts))
            response = updateProperty(guid, value, opts)
            responses.append(response)

    return responses


##### Do not need #####
class Update(object):
    def __init__(self, opts, data, httpConfig=None):
        raise NotImplementedError("Update is not implemented")

class InitiativeUpdate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("InitiativeUpdate is not implemented")

class FrameworkUpdate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("FrameworkUpdate is not implemented")

class SetUpdate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("SetUpdate is not implemented")

class DomainUpdate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("DomainUpdate is not implemented")

class ClusterUpdate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("ClusterUpdate is not implemented")

class StandardUpdate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("StandardUpdate is not implemented")

class ComponentUpdate(Insert):
    def __init__(self, opts, data):
        raise NonImplementedError("ComponentUpdate is not implemented")

class StrandUpdate(Insert):
    def __init__(self, opts, data):
        raise NonImplementedError("StrandUpdate is not implemented")

class SectionUpdate(Insert):
    def __init__(self, opts, data):
        raise NonImplementedError("SectionUpdate is not implemented")

class AnchorUpdate(Insert):
    def __init__(self, opts, data):
        raise NonImplementedError("AnchorUpdate is not implemented")

class CompetencyUpdate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("CompetencyUpdate is not implemented")

class ContainerUpdate(Insert):
    def __init__(self, opts, data):
        raise NotImplementedError("ContainerUpdate is not implemented")
