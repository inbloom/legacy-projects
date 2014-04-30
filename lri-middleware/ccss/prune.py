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
# Prune
###############################################################################

class PrunerFactory(object):
    def CreatePruner(self, pathInfo, opts):
        """Returns appropriate Pruner object"""

        pruner = None

        key = pathInfo.lstrip("/")
        if key in [
            "initiatives",
            "grade_levels",
            "competency_containers",
            "competencys",
            "strands",
            "standard_components",
            "anchor_standards",
            "learning_resources", 
            "competency_paths"
            ]:
            pruner = GenericPruner(key)
        elif key == "frameworks":
            pruner = FrameworkPruner(key)
        elif key == "sets":
            pruner = SetPruner(key)
        elif key == "domains":
            pruner = DomainPruner(key)
        elif key == "clusters":
            pruner = ClusterPruner(key)
        elif key == "standards":
            pruner = StandardPruner(key)
            gradeLevel = ""
            if "grade_level" in opts:
                pruner.setGradeLevel(opts["grade_level"])
        elif key == "standard_components":
            pruner = ComponentPruner(key)
        elif key == "anchor_standard_sections":
            pruner = SectionPruner(key)
        elif key == "anchor_standards":
            pruner = AnchorPruner(key)
        elif key.find("property_names") != -1:
            pruner = PropertyPruner("property_names")
                        
        return pruner

class Pruner(object):
    """Base class for prune"""

    def __init__(self, key=None):
        # self.key: Tucks results under key
        self.key = key
        self.pruner_type = "Pruner"

    def prune(self, queryResult, keep=None):
        """Removes duplicates and flattens structure. Returns dict

To be implemented by subclasses

"""
        pass

class GenericPruner(Pruner):
    """Prunes common types"""

    def __init__(self, key):
        Pruner.__init__(self, key)
        self.pruner_type = "GenericPruner"

    def prune(self, queryResult, keep=None):
        """Returns new dict w/key for pruned results"""

        newReq = {}
        newReq["response"] = []
        newReq["response"].append({})
        newReq["response"][0][self.key] = queryResult.get("response")
        newReq["status"] = queryResult.getStatus()

        queryResult.setData(newReq)

        return queryResult

class FrameworkPruner(GenericPruner):
    """For pruning CCSS frameworks"""

    def __init__(self, key):
        GenericPruner.__init__(self, key)
        self.pruner_type = "FrameworkPruner"

    def prune(self, queryResult, keep=None):
        """Returns new dict w/key for pruned framework results"""

        result = GenericPruner.prune(self, queryResult, keep)
        r = result.getData()
        for framework in r["response"][0][self.key]:
            frameworkId = framework["props"]["urn:lri:property_type:id"]
            if frameworkId == "urn:ccss:framework:CCSS.ELA-Literacy":
                framework["child_type"] = "urn:ccss:entity:type:domain"
            else:
                framework["child_type"] = "urn:ccss:entity:type:set"

        return result

class SetPruner(Pruner):
    """For pruning CCSS sets"""

    def __init__(self, key):
        Pruner.__init__(self, key)
        self.pruner_type = "SetPruner"

    def prune(self, queryResult, keep=None):
        """Returns new dict w/key for pruned set results"""

        entities = []
        for entity in queryResult.get("response"):
            if "urn:ccss:entity_type:set" in entity["props"]["urn:lri:property_type:types"]:
                entities.append(entity)

        # Flatten
        r = {}
        r["response"] = []
        r["response"].append({})
        r["response"][0][self.key] = entities
        r["status"] = queryResult.getStatus()

        queryResult.setData(r)

        return queryResult

class DomainPruner(Pruner):
    """For pruning CCSS domains"""

    def __init__(self, key):
        Pruner.__init__(self, key)
        self.pruner_type = "DomainPruner"
        self.prop = "urn:lri:property_type:competency_in_path"

    def prune(self, queryResult, keep=None):
        """Returns new dict w/key for pruned domain results"""

        domains = []
        for path in queryResult.get("response"):
            if "urn:lri:property_type:path_step" in path["props"]:
                # For domains from grade paths
                for step in path["props"]["urn:lri:property_type:path_step"]:
                    for domain in step["props"][self.prop]:
                        domains.append(domain)
            else:
                # For math domains from grade_levels
                domains.append(path)

        # Flatten
        r = {}
        r["response"] = []
        r["response"].append({})
        r["response"][0][self.key] = domains
        r["status"] = queryResult.getStatus()

        queryResult.setData(r)

        return queryResult
        
    def pruneOld(self, queryResult, keep=None):
        raise DeprecatedError("DomainPruner.pruneOld is deprecated")

        newReq = {}
        newReq["response"] = []
        i = 0
        for resp in queryResult.get("response"):
            newReq["response"].append({})
            newReq["response"][i] = {}
            newReq["response"][i][self.key] = []
            newReq["response"][i][self.key] = resp["props"][self.prop]
            i += 1
        newReq["status"] = queryResult.getStatus()

        queryResult.setData(newReq)

        return queryResult

class ClusterPruner(Pruner):
    """For pruning CCSS clusters"""

    def __init__(self, key):
        Pruner.__init__(self, key)
        self.pruner_type = "ClusterPruner"

    def prune(self, queryResult, keep=None):
        """Returns new dict w/key for pruned cluster results"""

        entities = []
        for entity in queryResult.get("response"):
            # Domains contain clusters and standards
            # Do not want to include standards in results
            if "urn:ccss:entity_type:standard" not in entity["props"]["urn:lri:property_type:types"]:
                entities.append(entity)

        # Flatten
        r = {}
        r["response"] = []
        r["response"].append({})
        r["response"][0][self.key] = entities
        r["status"] = queryResult.getStatus()

        queryResult.setData(r)

        return queryResult
        
    def pruneOld(self, queryResult, keep=None):
        raise DeprecatedError("ClusterPruner.pruneOld is deprecated")

        clusters = []
        cluster_ids = []
        for resp in queryResult.get("response"):
            for standard in resp["props"]["urn:lri:property_type:contains"]:
                for cluster in standard["props"]["urn:lri:property_type:cluster"]:
                    if cluster["props"]["urn:lri:property_type:id"] not in cluster_ids:
                        cluster_ids.append(cluster["props"]["urn:lri:property_type:id"])
                        clusters.append(cluster)

        # Flatten
        new_req = {}
        new_req["response"] = []
        new_req["response"].append({})
        new_req["response"][0] = {}
        new_req["response"][0][self.key] = clusters
        new_req["status"] = queryResult.getStatus()
        queryResult.setData(new_req)

        return queryResult

class StandardPruner(Pruner):
    """For pruning CCSS standards"""

    def __init__(self, key):
        Pruner.__init__(self, key)
        # self.gradeLevel
        # Used to prune results
        self.gradeLevel = None
        self.pruner_type = "StandardPruner"

    def setGradeLevel(self, gradeLevelId):
        """Sets gradeLevel to be used to prune results"""

        self.gradeLevel = gradeLevelId

    def parseCcid(self, ccid):
        """Parses CCID into struct

ELA keys:
* initiative
* framework
* domain
* grade_level
* num

Math keys:
* initiative
* framework
* grade_level
* domain
* cluster
* num
"""

        ccidStruct = {}
        if ccid.find("ELA-Literacy") != -1:
            initiative, framework, domain, grade, num = ccid.split(".")
            ccidStruct["initiative"] = initiative
            ccidStruct["framework"] = framework
            ccidStruct["domain"] = domain
            ccidStruct["grade_level"] = grade
            ccidStruct["num"] = num

        elif ccid.find("Math.Content") != -1:
            initiative, framework, set, grade, domain, cluster, num = ccid.split(".")
            ccidStruct["initiative"] = initiative
            ccidStruct["framework"] = framework
            ccidStruct["grade_level"] = grade
            ccidStruct["domain"] = domain
            ccidStruct["cluster"] = cluster
            ccidStruct["num"] = num

        return ccidStruct

    def pruneEla(self, queryResult):
        """Prunes CCSS ELA standards"""

        print("StandardPruner.pruneEla")

        print("StandardPruner.pruneEla: Pruning %d standards (1)" % len(queryResult.get("response")))
        for standard in queryResult.get("response"):
            if "urn:lri:property_type:contained_by" in standard["props"]:
                containedBy = standard["props"]["urn:lri:property_type:contained_by"]
                if type(containedBy) == list:
                    for parentType in containedBy:
                        if parentType.find(":domain:") != -1:
                            return self.pruneElaSB(queryResult)
                elif containedBy.find(":domain:") != -1:
                    return self.pruneElaSB(queryResult)

        standards = []
        print("StandardPruner.pruneEla: Pruning %d standards (2)" % len(queryResult.get("response")))
        for standard in queryResult.get("response"):
            standards.append(standard)

        print("StandardPruner.pruneEla: Pruned %d standards" % len(standards))

        return standards

    def pruneElaSB(self, queryResult):
        """Prunes CCSS ELA standards as used by Standards Browser"""

        print("StandardPruner.pruneElSB")

        standards = []
        for grade in queryResult.get("response"):
            gradeLevel = grade["props"]["urn:lri:property_type:id"]

            for standard in grade["props"]["urn:lri:property_type:contains"]:
                if gradeLevel == self.gradeLevel:
                    standards.append(standard)

        print("StandardPruner.pruneElaSB: Pruned %d standards" % len(standards))

        return standards

    def pruneMath(self, queryResult):
        """Prunes CCSS Math standards"""

        standards = []
        for standard in queryResult.get("response"):
            if "urn:ccss:entity_type:standard" in standard["props"]["urn:lri:property_type:types"]:
                standards.append(standard)
            
        return standards

    def pruneCustom(self, queryResult):
        """Prunes custom standards"""

        print("StandardPruner.pruneCustom")

        standards = []
        for standard in queryResult.get("response"):
            standards.append(standard)

        print("StandardPruner.pruneCustom: Pruned %d standards" % len(standards))

        return standards

    def prune(self, queryResult, keep=None):
        """Returns new dict w/key for pruned standard results"""

        print("StandardPruner.prune")

        standards = []
        print("StandardPruner.prune: Number of un-pruned standards: %d" % len(queryResult.get("response")))
        for item in queryResult.get("response"):
            print
            # If item has a CCID it is a CCSS type
            if "urn:ccss:property_type:ccid" in item["props"]:
                ccid = item["props"]["urn:ccss:property_type:ccid"]
                print("StandardPruner.prune: Pruning CCSS item: %s" % ccid)

                if ccid.find("ELA-Literacy") != -1:
                    # Prune CCSS ELA structure
                    print("StandardPruner.prune: Pruning CCSS ELA item: %s" % ccid)

                    if "urn:lri:property_type:contained_by" in item["props"]:
                        containedBy = item["props"]["urn:lri:property_type:contained_by"]
                        if type(containedBy) == list:
                            # contained_by can be list
                            print("StandardPruner.prune: contained_by is list")
                            for parentType in containedBy:
                                if parentType.find(":domain:") != -1:
                                    # contained_by domain means this is a grade_level
                                    # grade_level contains standard
                                    itemId = item["props"]["urn:lri:property_type:id"]
                                    print("StandardPruner.prune: item ccid       = %s" % ccid)
                                    print("StandardPruner.prune: item id         = %s" % itemId)
                                    print("StandardPruner.prune: self.gradeLevel = %s" % self.gradeLevel)

                                    for standard in item["props"]["urn:lri:property_type:contains"]:
                                        standardId = standard["props"]["urn:lri:property_type:id"]
                                        standardParent = standard["props"]["urn:lri:property_type:contained_by"]
                                        print("StandardPruner.prune:   standard = %s" % standardId)
                                        print("StandardPruner.prune:   contained_by = %s" % standardParent)
                                        if itemId == self.gradeLevel:
                                            print("StandardPruner.prune:     Match: %s == %s" % (itemId, self.gradeLevel))
                                            standards.append(standard)
                        else:
                            print("StandardPruner.prune: contained_by is scalar")
                            print("StandardPruner.prune: contained_by: %r" % item["props"]["urn:lri:property_type:contained_by"])

                            if containedBy.find(":domain:") != -1:
                                # contained_by domain means this is a grade_level
                                # grade_level contains standard
                                itemId = item["props"]["urn:lri:property_type:id"]
                                print("StandardPruner.prune: contained_by    = %s" % containedBy)
                                print("StandardPruner.prune: item ccid       = %s" % ccid)
                                print("StandardPruner.prune: item id         = %s" % itemId)
                                print("StandardPruner.prune: self.gradeLevel = %s" % self.gradeLevel)
                                for standard in item["props"]["urn:lri:property_type:contains"]:
                                    standardId = standard["props"]["urn:lri:property_type:id"]
                                    standardParent = standard["props"]["urn:lri:property_type:contained_by"]
                                    print("StandardPruner.prune:   standard     = %s" % standardId)
                                    print("StandardPruner.prune:   contained_by = %s" % standardParent)
                                    if itemId == self.gradeLevel:
                                        print("StandardPruner.prune:     Match: %s == %s" % (itemId, self.gradeLevel))
                                        standards.append(standard)

                            elif containedBy.find(":grade") != -1:
                                # contained_by grade_level means this is a standard
                                itemId = item["props"]["urn:lri:property_type:id"]
                                contains = item["props"]["urn:lri:property_type:contains"];
                                print("StandardPruner.prune: contained_by    = %s" % containedBy)
                                print("StandardPruner.prune: item ccid       = %s" % ccid)
                                print("StandardPruner.prune: item id         = %s" % itemId)
                                standards.append(item)

                elif ccid.find("Math") != -1:
                    # Prune CCSS Math structure
                    print("StandardPruner.prune: Pruning CCSS Math item: %s" % ccid)
                    if "urn:ccss:entity_type:standard" in item["props"]["urn:lri:property_type:types"]:
                        standards.append(item)
            else:
                # Custom standards will not have ccid
                if "urn:ccss:entity_type:standard" in item["props"]["urn:lri:property_type:types"]:
                    standards.append(item)

        print("StandardPruner.prune: Pruned %d standards" % len(standards))

        # Flatten
        r = {}
        r["response"] = []
        r["response"].append({})
        r["response"][0][self.key] = standards
        r["status"] = queryResult.getStatus()

        queryResult.setData(r)

        return queryResult
            
    def pruneElaOld(self, queryResult):
        raise DeprecatedError("StandardPruner.pruneOld is deprecated")

        # Flatten
        newReq = {}
        newReq["response"] = []
        i = 0
        standardIds = []
        anchorIds = []
        for resp in queryResult.get("response"):
            newReq["response"].append({})
            newReq["response"][i] = {}
            newReq["response"][i][self.key] = []
            sectionCcid = resp["props"]["urn:lri:property_type:ccid"]
            sectionCcidParts = sectionCcid.split(".")
            for anchor in resp["props"]["urn:lri:property_type:contained_anchor_standard"]:
                for standard in anchor["props"]["urn:lri:property_type:anchors"]:
                    standardCcid = standard["props"]["urn:lri:property_type:ccid"]
                    standardCcidParts = standardCcid.split(".")
                    if standardCcidParts[0] == sectionCcidParts[0]:
                        if standardCcidParts[1] == sectionCcidParts[1]:
                            standardId = standard["props"]["urn:lri:property_type:id"]
                            if standardId not in standardIds:
                                standardIds.append(standardId)

                                # anchor
                                anchorName = anchor["props"]["urn:lri:property_type:name"]
                                anchorCcid = anchor["props"]["urn:lri:property_type:ccid"]
                                anchorDesc = anchor["props"].get("urn:lri:property_type:description", "TBD")

                                standard["props"]["anchor_standard"] = {}
                                standard["props"]["anchor_standard"]["urn:lri:property_type:name"] = anchorName
                                standard["props"]["anchor_standard"]["urn:lri:property_type:ccid"] = anchorCcid
                                standard["props"]["anchor_standard"]["urn:lri:property_type:description"] = anchorDesc
                                newReq["response"][i][self.key].append(standard)
            i += 1
        newReq["status"] = queryResult.getStatus()

        return newReq

    def pruneMathOld(self, queryResult):
        raise DeprecatedError("StandardPruner.pruneMathOld is deprecated")

        # Flatten
        newReq = {}
        newReq["response"] = []
        i = 0
        for resp in queryResult.get("response"):
            newReq["response"].append({})
            newReq["response"][i] = {}
            components = []
            newReq["response"][i][self.key] = resp["props"]["urn:lri:property_type:standard"]
            i += 1
        newReq["status"] = queryResult.getStatus()

        return newReq

    def pruneOld(self, queryResult, keep=None):
        raise DeprecatedError("StandardPruner.pruneOld is deprecated")

        pruneEla = False
        for response in queryResult.get("response"):
            if response["props"]["urn:lri:property_type:subject"] == "urn:ccss/subject/ela":
                pruneEla = True

        newReq = {}
        if pruneEla:
            newReq = self.pruneElaOld(queryResult)
        else:
            newReq = self.pruneMathOld(queryResult)
        queryResult.setData(newReq)

        return queryResult

class ComponentPruner(Pruner):
    """For pruning CCSS stanard_components"""

    def __init__(self, key):
        Pruner.__init__(self, key)
        self.prop = "urn:lri:property_type:contains"
        self.pruner_type = "ListPruner"

    def prune(self, queryResult, keep=None):
        """Returns new dict w/key for pruned standard_component results

Prunes by self.prop

"""

        # Flatten
        newReq = {}
        newReq["response"] = []
        i = 0
        for resp in queryResult.get("response"):
            newReq["response"].append({})
            newReq["response"][i] = {}
            newReq["response"][i][self.key] = resp["props"][self.prop]
        i += 1
        newReq["status"] = queryResult.getStatus()
        queryResult.setData(newReq)

        return queryResult

class SectionPruner(Pruner):
    """For pruning CCSS anchor_standard_sections"""

    def __init__(self, key):
        Pruner.__init__(self, key)
        self.pruner_type = "SectionPruner"

    def prune(self, queryResult, keep=None):
        """Returns new dict w/key for pruned anchor_standard_section results"""

        # Flatten
        newReq = {}
        newReq["response"] = []
        i = 0
        sectionIds = []
        for resp in queryResult.get("response"):
            newReq["response"].append({})
            newReq["response"][i] = {}
            newReq["response"][i][self.key] = []
            domainCcid = resp["props"]["urn:lri:property_type:ccid"]
            domainCcidParts = domainCcid.split(".")
            for standard in resp["props"]["urn:lri:property_type:contains"]:
                for anchor in standard["props"]["urn:lri:property_type:is_anchored_to"]:
                    for section in anchor["props"]["urn:lri:property_type:is_in_section"]:
                        sectionCcid = section["props"]["urn:lri:property_type:ccid"]
                        sectionCcidParts = sectionCcid.split(".")
                        if sectionCcidParts[0] == domainCcidParts[0]:
                            if sectionCcidParts[1] == domainCcidParts[1]:
                                sectionId = section["props"]["urn:lri:property_type:id"]
                                if sectionId not in sectionIds:
                                    sectionIds.append(sectionId)
                                    newReq["response"][i][self.key].append(section)
            i += 1
        newReq["status"] = queryResult.getStatus()
        queryResult.setData(newReq)

        return queryResult

class AnchorPruner(Pruner):
    """For pruning CCSS anchor_standards"""

    def __init__(self, key):
        Pruner.__init__(self, key)
        # Property to prune by
        self.prop = "urn:lri:property_type:contained_anchor_standard"
        self.pruner_type = "AnchorPruner"

    def prune(self, queryResult, keep=None):
        """Returns new dict w/key for pruned anchor_standard results"""

        # Flatten
        newReq = {}
        newReq["response"] = []
        i = 0
        for resp in queryResult.get("response"):
            newReq["response"].append({})
            newReq["response"][i] = {}
            newReq["response"][i][self.key] = []
            for item in resp["props"][self.prop]:
                newReq["response"][i][self.key].append(item)
            i += 1
        newReq["status"] = queryResult.getStatus()
        queryResult.setData(newReq)

        return queryResult

class PropertyPruner(Pruner):
    """For pruning property list"""

    def __init__(self, key):
        Pruner.__init__(self, key)
        self.pruner_type = "PropertyPruner"

    def prune(self, queryResult, keep=None):
        """ Prune properties"""

        # Flatten
        r = {}
        r["response"] = []
        r["response"].append({})
        r["response"][0][self.key] = queryResult.getPropertyNames()
        r["status"] = queryResult.getData()["status"]
        queryResult.setData(r)

        return queryResult
