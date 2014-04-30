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

###############################################################################
# LRI Query Wrappers
###############################################################################

import copy
import json
import requests
import web

# Local modules
import httpconfig
import utils

class QueryFactory(object):
    """Factory for creating Queries"""

    def CreateQuery(self, pathInfo, opts, httpConfig, limit=None):
        """Creates a Query based on PATH_INFO"""

        web.debug("QueryFactory.CreateQuery")
        web.debug("QueryFactory.CreateQuery: pathInfo = %s" % pathInfo)
        web.debug("QueryFactory.CreateQuery: opts     = %s" % opts)
        web.debug("QueryFactory.CreateQuery: limit   = %s" % limit)

        query = None
        if pathInfo == "/initiatives":
            query = InitiativeQuery(opts, httpConfig)
        elif pathInfo == "/frameworks":
            query = FrameworkQuery(opts, httpConfig)
        elif pathInfo == "/sets":
            query = SetQuery(opts, httpConfig)
        elif pathInfo == "/grade_levels":
            query = GradeQuery(opts, httpConfig)
        elif pathInfo == "/competency_containers":
            query = ContainerQuery(opts, httpConfig)
        elif pathInfo == "/competencys":
            query = CompetencyQuery(opts, httpConfig)
        elif pathInfo == "/domains":
            query = DomainQuery(opts, httpConfig)
        elif pathInfo == "/clusters":
            query = ClusterQuery(opts, httpConfig)
        elif pathInfo == "/standards":
            query = StandardQuery(opts, httpConfig)
        elif pathInfo == "/standard_components":
            query = ComponentQuery(opts, httpConfig)

        elif pathInfo == "/strands":
            query = StrandQuery(opts, httpConfig)
        elif pathInfo == "/anchor_standards":
            query = AnchorQuery(opts, httpConfig)
        elif pathInfo == "/anchor_standard_sections":
            query = SectionQuery(opts, httpConfig)

        elif pathInfo in ["/competency_paths", "/competency_path/"]:
            query = PathQuery(opts, httpConfig)
        elif pathInfo in ["/learning_resources", "/learning_resource/"]:
            query = ResourceQuery(opts, httpConfig)


        elif pathInfo.find("/property_names") != -1:
            # Get singular type name
            lriType = pathInfo.split("/property_names")[0].strip("/").rstrip("s")
            query = PropertyQuery(lriType, opts, httpConfig)

        if limit is not None:
            query.setLimit(limit)

        #web.debug("QueryFactory.CreateQuery: query = %r" % query)
        return query

class Query(object):
    """Base Query class for gets"""

    def __init__(self, opts, httpConfig=None):
        web.debug("Query.__init__")

        self.path = "entity/search"
        self.opts = {}

        # Some queries are composed of multiple queries
        self.query = ""
        self.queries = []

        self.url = ""
        self.httpConfig = httpConfig
        if self.httpConfig is None:
            self.httpConfig = httpconfig.HttpConfig(web.ctx.env["DOCUMENT_ROOT"])
        self.limit = None

    def __repr__(self):
        return "<Query('%r', '%r')>" % (self.opts, self.httpConfig)

    def __str__(self):
        return "query: %s, queries: %r, url: %s" % (self.query, self.queries, 
                                                    self.url)

    def setLimit(self, limit):
        self.limit = limit

    def toUrlForm(self, query=None):
        """Assembles URL"""

        if query is None:
            if len(self.queries) == 0:
                if isinstance(self.query, list):
                    # Standards
                    query = self.query[0]
                else:
                    query = self.query
            else:
                query = self.queries[0]

        self.url = "http://%s:%d/%s?q=%s&opts=%s" % (self.httpConfig.config["serverhost"], 
                                                     self.httpConfig.config["serverport"], 
                                                     self.path, query, 
                                                     json.dumps(self.opts))

        if self.limit is not None:
            self.url = self.url.replace('{', '{"limit":%d,' % self.limit, 1)

        return self.url

    def getUrl(self):
        """Returns URL that can be sent to LRI server"""

        return self.toUrlForm()

    def getUrls(self):
        urls = []
        for query in self.queries:
            urls.append(self.toUrlForm(query))
        return urls

    def parseOpts(self, opts, key):
        """Extracts key from opts and returns tuple of (value, modified opts)"""

        ID = None
        optsCopy = copy.deepcopy(opts)
        if optsCopy.has_key(key):
            ID = '"%s"' % optsCopy[key]
            del(optsCopy[key])

        return ID, optsCopy

    def parseOptsList(self, opts, keyList):
        """Extracts key in list of keys from opts and returns tuple of (value, modified opts)"""

        ID = None
        optsCopy = copy.deepcopy(opts)
        for key in keyList:
            if key in optsCopy:
                ID = '"%s"' % optsCopy[key]
                break

        for key in keyList:
            if key in optsCopy:
                del(optsCopy[key])

        return ID, optsCopy

    def getParentType(self, parentId):
        return parentId.split("/")[3]

class InitiativeQuery(Query):
    """Query for getting initiatives"""

    def __init__(self, opts, httpConfig):
        Query.__init__(self, opts, httpConfig)
        self.opts = opts
        self.query = '{"urn:lri:property_type:types":"urn:ccss:entity_type:initiative"}'

    def __repr__(self):
        return "InitiativeQuery<('%r', '%r')>" % (self.opts, self.httpConfig)

    def __str__(self):
        return "query: %s, queries: %r, url: %s" % (self.query, self.queries, 
                                                    self.url)
class FrameworkQuery(Query):
    """Query for getting frameworks in an initiative"""

    def __init__(self, opts, httpConfig):
        Query.__init__(self, opts, httpConfig)
        initiativeId, self.opts = self.parseOpts(opts, "initiative");
        if initiativeId:
            self.query = '{"urn:lri:property_type:contained_by":%s}' % initiativeId
        else:
            self.query = '{"urn:lri:property_type:types":"urn:ccss:entity_type:framework"}'

class SetQuery(Query):
    """Query for getting sets in a framework

Takes a framework id

"""

    def __init__(self, opts, httpConfig):
        Query.__init__(self, opts, httpConfig)
        frameworkId, self.opts = self.parseOpts(opts, "framework")
        if frameworkId:
            self.query = '{"urn:lri:property_type:contained_by":%s}' % frameworkId
        else:
            self.query = '{"urn:lri:property_type:types":"urn:ccss:entity_type:set"}'

class GradeQuery(Query):
    """Query for getting grade_levels"""

    def __init__(self, opts, httpConfig):
        """Query for getting Math and ELA grade_levels"""
        web.debug("GradeQuery.__init__")

        mapping = {
            '"urn:ccss:framework:CCSS.ELA-Literacy"': '"urn:ccss:ordering:CCSS.ELA-Literacy"',
            '"urn:ccss:framework:CCSS.Math"': '"urn:ccss:ordering:CCSS.Math.Content"'
            }

        Query.__init__(self, opts, httpConfig)
        parentId, self.opts = self.parseOptsList(opts, ["framework", "set", "domain"])
        web.debug("GradeQuery.__init__: parentId  = %s" % parentId)
        web.debug("GradeQuery.__init__: self.opts = %s" % self.opts)

        if parentId:
            if parentId in mapping:
                self.query = '{"urn:lri:property_type:id":%s,"shape":{"urn:lri:property_type:path_step":{"urn:lri:property_type:path_step":{}}}}' % mapping[parentId]
            else:
                self.query = '{"urn:lri:property_type:contained_by":%s,"shape":{"urn:lri:property_type:contains":{}}}' % parentId
        else:
            self.query = '{"urn:lri:property_type:types":"urn:ccss:entity_type:grade_level"}'


class ContainerQuery(Query):
    def __init__(self, opts, httpConfig):
        Query.__init__(self, opts, httpConfig)
        parentId, self.opts = self.parseOptsList(opts, ["parent"])
        self.query = '{"urn:lri:property_type:contained_by":%s}' % parentId

class CompetencyQuery(Query):
    def __init__(self, opts, httpConfig):
        Query.__init__(self, opts, httpConfig)
        parentId, self.opts = self.parseOptsList(opts, ["parent"])
        self.query = '{"urn:lri:property_type:contained_by":%s}' % parentId

class DomainQuery(Query):
    """Query for getting Math and ELA domains"""

    def __init__(self, opts, httpConfig):
        """Query for getting domains

Math:
/ccss/domains?grade_level=urn:ccss:ordering:CCSS.Math.Content:K

ELA:
/ccss/domains?grade_level=urn:ccss:ordering:CCSS.ELA-Literacy:K
returns name=NAME, id=GRADE_LEVEL_ID:DOMAIN_ID

"""

        Query.__init__(self, opts, httpConfig)
        parentId, self.opts = self.parseOptsList(opts, ["grade_level", "framework"])

        # Math
        web.debug(parentId)
        if parentId:
            if parentId.find("ordering") != -1:
                self.query = '{"urn:lri:property_type:id":%s,"shape":{"urn:lri:property_type:path_step":{"urn:lri:property_type:competency_in_path":{}}}}' % parentId
            else:
                self.query = '{"urn:lri:property_type:contained_by":%s}' % parentId
        else:
            self.query = '{"urn:lri:property_type:types":"urn:ccss:entity_type:domain"}'



    def getRelationshipId(self, parentId):
        relationshipId = ""
        parentType = self.getParentType(parentId)

        # In v0.2 schema grade_level ids have type "grade", not "grade_level"
        if parentType in ["grade", "framework"]:
            relationshipId = '"urn:lri:property_type:contained_by"'
        elif parentType == "strand":
            relationshipId = '"urn:ccss:property_type:is_in_strand"'

        return relationshipId

class ClusterQuery(Query):
    """Query for getting Math clusters

Takes domain id

"""

    def __init__(self, opts, httpConfig):
        Query.__init__(self, opts, httpConfig)
        domainId, self.opts = self.parseOpts(opts, "domain")
        if domainId:
            self.query = '{"urn:lri:property_type:contained_by":%s,"shape":{"urn:lri:property_type:contains":{}}}' % domainId
        else:
            self.query = '{"urn:lri:property_type:types":"urn:ccss:entity_type:cluster"}'


class StandardQuery(Query):
    """Query for getting Math and ELA standards

Takes: domain id, cluster id, grade_level id, anchor_standard id, or competency_container id

"""

    def __init__(self, opts, httpConfig):
        Query.__init__(self, opts, httpConfig)
        self.grade_level = None
        if "grade_level" in opts:
            self.grade_level = opts["grade_level"]

        self.parentId, self.relationship, self.getChildren, self.getAnchors, self.opts = self.parseOpts(opts, ["domain", "cluster", "grade_level", "anchor_standard", "competency_container"])
        print("StandardQuery.__init__: self.opts = %r" % self.opts)

        if self.parentId:
            self.query = '{%s:%s}' % (self.relationship, self.parentId)
        else:
            self.query = ['{"urn:lri:property_type:types":"urn:ccss:entity_type:standard"}']

        web.debug("StandardQuery: self.query = %s" % self.query)

    def getEntityById(self, entityId):
        """Gets entity from LRI

entityId: ID of the entity to get
returns: JSON of the entity

"""
        entities = []

        q = '{"urn:lri:property_type:id":"%s"}' % entityId
        url = self.toUrlForm(q)
        print("StandardQuery.getEntityById: Running query: %s" % url)
        results = requests.get(url)
        statusCode = results.status_code
        j = utils.getJson(results)
        response = j["response"]
        for entity in response:
            entityId = entity["props"]["urn:lri:property_type:id"]
            entities.append(entity)
            print("StandardQuery.getEntityById:    Added entity: %s" % entityId)
        print("StandardQuery.getEntityById: Got %d entity(s)" % len(entities))

        if len(entities) > 1:
            print("StandardQuery.getEntityById: ERROR: Too many entities: %d from id: %d" % (len(entities), entityId))

        entity = None
        try:
            entity = entities[0]
        except IndexError, e:
            raise IndexError("ERROR getting: %s" % entityId)

        return entity

    def getStandards(self):
        """Gets standards from LRI

returns: JSON of the standards

"""

        print("StandardQuery.getStandards")

        print("StandardQuery.getStandards: self.opts = %r" % self.opts)

        print("StandardQuery.getStandards: Running query: %s" % self.toUrlForm())
        results = requests.get(self.toUrlForm())
        statusCode = results.status_code
        j = utils.getJson(results)
        print("StandardQuery.getStandards: j=",j)
        response = j["response"]

        # Get standards
        standards = []
        for item in response:
            print
            itemId = item["props"]["urn:lri:property_type:id"]
            print("StandardQuery.getStandards:    Processing: %s" % itemId)

            # If item has a CCID it is a CCSS type
            if "urn:ccss:property_type:ccid" not in item["props"]:
                # Custom standards will not have ccid
                print("StandardQuery.getStandards:       Processing Custom item: %s" % itemId)

                # Custom standards will be type competency
                customType = "urn:lri:entity_type:competency"
                if customType in item["props"]["urn:lri:property_type:types"]:
                    standards.append(item)
                    print("StandardQuery.getStandards:          Added Custom standard: %s" % itemId)
                else:
                    print("StandardQuery.getStandards: ERROR: type: %s not in: %r" % (customType,
                                                                                      item["props"]["urn:lri:property_type:types"]))

            else:
                ccid = item["props"]["urn:ccss:property_type:ccid"]
                print("StandardQuery.getStandards:    Processing CCSS item: %s" % ccid)

                if ccid.find("Math") != -1:
                    # Prune CCSS Math structure
                    print("StandardQuery.getStandards:       Processing CCSS Math item: %s" % ccid)
                    if "urn:ccss:entity_type:standard" in item["props"]["urn:lri:property_type:types"]:
                        standards.append(item)
                    print("StandardQuery.getStandards:          Added CCSS Math standard: %s" % itemId)

                elif ccid.find("ELA-Literacy") != -1:
                    # Prune CCSS ELA structure
                    print("StandardQuery.getStandards:       Processing CCSS ELA item: %s" % ccid)

                    cbProp = "urn:lri:property_type:contained_by"
                    containedBy = item["props"][cbProp]
                    if type(containedBy) == str or type(containedBy) == unicode:
                        containedBy = [containedBy]

                    # Handle contained_by domain or grade_level
                    for cb in containedBy:
                        print("StandardQuery.getStandards:    contained_by = %s" % cb)

                        if cb.find(":domain:") != -1:
                            # contained_by domain means item is grade_level
                            # grade_level contains standard
                            gradeId = item["props"]["urn:lri:property_type:id"]
                            print("StandardQuery.getStandards:       Checking: (%s, %s)" % (self.grade_level, gradeId))
                            if gradeId == self.grade_level:
                                print("StandardQuery.getStandards:          Processing grade_level: %s" % gradeId)

                                for standardId in item["props"]["urn:lri:property_type:contains"]:
                                    print("StandardQuery.getStandards:             Processing CCSS ELA standard: %s" % standardId)

                                    standard = self.getEntityById(standardId)
                                    standards.append(standard)
                                    newId = standard["props"]["urn:lri:property_type:id"]
                                    if newId != standardId:
                                        print("StandardQuery.getStandards: ERROR: %s != %s" % (newId, standardId))
                                    print("StandardQuery.getStandards:             Added CCSS ELA standard: %s, (domain = %s, grade = %s)" % (newId, cb, gradeId))
                            else:
                                print("StandardQuery.getStandards:          Skipping grade_level: %s" % gradeId)


                        elif cb.find(":grade") != -1:
                            # contained_by grade_level means item is standard
                            standard = self.getEntityById(itemId)
                            standards.append(standard)
                            newId = standard["props"]["urn:lri:property_type:id"]
                            if newId != itemId:
                                print("StandardQuery.getStandards: ERROR: %s != %s" % (newId, itemId))
                            print("StandardQuery.getStandards:             Added CCSS ELA standard: %s" % newId)

        print("StandardQuery.getStandards: Processed %d standards" % len(standards))

        # Get components
        if self.getChildren:
            print("StandardQuery.getStandards: Getting standard_components")

            for std in standards:
                if not "urn:lri:property_type:contains" in std["props"]:
                    continue

                stdId = std["props"]["urn:lri:property_type:id"]
                print("StandardQuery.getStandards:    Getting components of: %s" % stdId)

                components = []
                print("StandardQuery.getStandards:    contains: ")
                print(std["props"]["urn:lri:property_type:contains"])
                print("StandardQuery.getStandards:    /contains")
                contains = std["props"]["urn:lri:property_type:contains"]
                if type(contains) == str or type(contains) == unicode:
                    contains = [contains]
                for componentId in contains:
                    print("StandardQuery.getStandards:       Getting standard_component: %s" % componentId)

                    component = self.getEntityById(componentId)
                    components.append(component)
                    newId = component["props"]["urn:lri:property_type:id"]
                    if newId != componentId:
                        print("StandardQuery.getStandards: ERROR: %s != %s" % (newId, standardId))
                    std["props"]["urn:lri:property_type:contains"] = components

                print("StandardQuery.getStandards: Added: %s components to standard: %s" % (len(std["props"]["urn:lri:property_type:contains"]), stdId))

        # Get anchors
        if self.getAnchors:
            print("StandardQuery.getStandards: Getting anchor_standards")

            for std in standards:
                if not "urn:ccss:property_type:is_anchored_to" in std["props"]:
                    continue

                stdId = std["props"]["urn:lri:property_type:id"]
                print("StandardQuery.getStandards:    Getting anchor for: %s" % stdId)

                anchorId = std["props"]["urn:ccss:property_type:is_anchored_to"]
                anchor = self.getEntityById(anchorId)
                newId = anchor["props"]["urn:lri:property_type:id"]
                if newId != anchorId:
                    print("StandardQuery.getStandards: ERROR: %s != %s" % (newId, anchorId))
                std["props"]["urn:ccss:property_type:is_anchored_to"] = anchor

                print("StandardQuery.getStandards:         Set is_anchored_to: %s" % anchor)
        
        # Flatten
        r = {}
        r["response"] = []
        r["response"].append({})
        r["response"][0]["standards"] = standards
        r["status"] = "success"
        r["status_code"] = statusCode

        return r

    def parseOpts(self, opts, keyList):
        """Returns:
parentId: id of parent (containing) type
relationship: LRI relationship property b/t parent type and standard
getChildren: include children (contained) types (standard_component) in query
getAnchors: include anchor_standards in query
parsedOpts: opts w/keys removed

"""
        print("StandardQuery.parseOpts")
        print("StandardQuery.parseOpts: opts = %r" % opts)
        print("StandardQuery.parseOpts: keyList = %r" % keyList)

        print("StandardQuery.parseOpts: Getting: parentId")
        parentId, parsedOpts = Query.parseOptsList(self, opts, keyList)
        print("StandardQuery.parseOpts: parsedOpts = %r" % parsedOpts)

        print("StandardQuery.parseOpts: Getting: getChildren")
        getChildren, parsedOpts = Query.parseOpts(self, parsedOpts, "children")
        print("StandardQuery.parseOpts: parsedOpts = %r" % parsedOpts)

        print("StandardQuery.parseOpts: Getting: getAnchors")
        getAnchors, parsedOpts = Query.parseOpts(self, parsedOpts, "anchors")
        print("StandardQuery.parseOpts: parsedOpts = %r" % parsedOpts)

        relationship = ""
        parentType = ""
        if parentId:
            print("StandardQuery.parseOpts: Getting: relationship")

            parentType = parentId.split(":")[2]
            if parentType in ["domain", "cluster", "grade", "competency_container"]:
                relationship = '"urn:lri:property_type:contained_by"'
            elif "anchor_standard" == parentType:
                relationship = '"urn:ccss:property_type:is_anchored_to"'
        
        return parentId, relationship, getChildren, getAnchors, parsedOpts

class ComponentQuery(Query):
    """Query for getting standard_components

Takes a standard id

"""

    def __init__(self, opts, httpConfig):
        Query.__init__(self, opts, httpConfig)
        standardId, self.opts = self.parseOpts(opts, "standard")
        if standardId:
            self.query = '{"urn:lri:property_type:contained_by":%s}' % standardId
        else:
            self.query = '{"urn:lri:property_type:types":"urn:ccss:entity_type:standard_component"}'


class SectionQuery(Query):
    """Query for getting ELA anchor_standard_sections"""

    def __init__(self, opts, httpConfig):
        Query.__init__(self, opts, httpConfig)
        self.opts = opts
        self.query = '{"urn:lri:property_type:types":"urn:ccss:entity_type:anchor_standard_section"}'

class AnchorQuery(Query):
    """Query for getting ELA anchor_standards

Takes a strand id or a standard id

"""

    def __init__(self, opts, httpConfig):
        Query.__init__(self, opts, httpConfig)
        parentId, relationshipId, self.opts = self.parseOpts(opts, ["strand", "standard"])
        if parentId:
            self.query = '{%s:%s}' % (relationshipId, parentId)
        else:
            self.query = '{"urn:lri:property_type:types":"urn:ccss:entity_type:anchor_standard"}'


    def parseOpts(self, opts, keyList):
        parentId, parsedOpts = Query.parseOptsList(self, opts, keyList)

        relationshipId = ""
        if parentId:
            parentType = parentId.split(":")[2]       
            if "strand" == parentType:
                relationshipId = '"urn:ccss:property_type:anchor_standard_included_in_strand"'
            elif "standard" == parentType:
                relationshipId = '"urn:ccss:property_type:anchors"'

        return parentId, relationshipId, parsedOpts

class PathQuery(Query):
    """Query for getting competency_paths:

Possible queries:
* All paths
* Specific path by competency_path id
* Paths by author id
* Full properties of contained types w/children=true

"""

    def __init__(self, opts, httpConfig):
        Query.__init__(self, opts, httpConfig)
        self.query = '{'
        if opts.has_key("competency_path"):
            pathId, self.opts = self.parseOpts(opts, "competency_path")
            self.query += '"urn:lri:property_type:id":%s' % pathId
        elif opts.has_key("authored_by"):
            authorId, self.opts = self.parseOpts(opts, "authored_by")
            self.query += '"urn:lri:property_type:authored_by":%s' % authorId
        else:
            self.opts = opts
            self.query += '"urn:lri:property_type:types":"urn:lri:entity_type:competency_path"'

        # Add shape to finish query
        if "competency_path" in opts or "authored_by" in opts:
            self.query = '%s,"shape":{"urn:lri:property_type:path_step":{"urn:lri:property_type:competency_in_path":{' % self.query
            if "children" in opts:
                if opts["children"]:
                    self.query += '"urn:lri:property_type:contains":{}'
            self.query += '}}}'
        self.query += '}'

class ResourceQuery(Query):
    """Query for getting learning_resources:

Possible queries:
* All resources
* Specific resource by id
* Resources by competency id

"""

    def __init__(self, opts, httpConfig):
        Query.__init__(self, opts, httpConfig)
        if "learning_resource" in opts:
            resourceId, self.opts = self.parseOpts(opts, "learning_resource")
            self.query = '{"urn:lri:property_type:id":%s,"shape":{"urn:lri:property_type:teaches":{}}}' % resourceId
        elif "competency" in opts:
            competencyId, self.opts = self.parseOpts(opts, "competency")
            self.query = '{"urn:lri:property_type:teaches":%s}' % competencyId
        else :
            self.opts = opts
            self.query = '{"urn:lri:property_type:types":"urn:lri:entity_type:learning_resource","shape":{"urn:lri:property_type:teaches":{}}}'

class StrandQuery(Query):
    """Query for getting ELA strands

Takes a set id

"""

    def __init__(self, opts, httpConfig):
        Query.__init__(self, opts, httpConfig)
        setId, self.opts = self.parseOpts(opts, "set")
        if setId:
            self.query = '{"urn:lri:property_type:contained_by":%s}' % setId
        else:
            self.query = '{"urn:lri:property_type:types":"urn:ccss:entity_type:strand"}'


class PropertyQuery(Query):
    """Query for getting LRI type property names"""

    def __init__(self, lriType, opts, httpConfig):
        Query.__init__(self, opts, httpConfig)
        ns = "ccss"
        if lriType in ["competency", "competency_container", "competency_path", "learning_resource", "path_step"]:
            ns = "lri"
        self.query = '{"urn:lri:property_type:id":"urn:%s:entity_type:%s"}' % (ns, lriType)
