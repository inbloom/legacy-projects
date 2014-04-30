###############################################################################
# Sort
###############################################################################

import copy
import re
import web

class SorterFactory(object):
    def CreateSorter(self, pathInfo, queryResult=None):
        """Given PATH_INFO and QueryResult, returns one of:
NameSorter (for sorting QueryResult by name)
PathSorter (for sorting path_steps in competency_paths in QueryResult)
CcidSorter (for sorting types in QueryResult by CCID)
DomainSorter (for sorting domains in QueryResult by CCID)
ClusterSorter (for sorting clusters in QueryResult by CCID)
StandardSorter (for sorting standards in QueryResult by CCID)
ComponentSorter (for sorting standard_components in QueryResult by CCID)
SectionSorter (for sorting anchor_standard_sections in QueryResult by CCID)
AnchorSorter (for sorting anchor_standards in QueryResult by CCID)
ResourceSorter (for sorting learning_resources in QueryResult by CCID)
StrandSorter (for sorting strands in QueryResult by CCID)

"""

        sorter = None

        key = pathInfo.strip("/")
        if pathInfo in ["/subjects", "/learning_resources", "/strands"]:
            sorter = NameSorter(key, queryResult)
        elif pathInfo in ["/competency_paths", "/grade_levels"]:
            if queryResult is not None:
                #web.debug("SorterFactory: CreateSorter: ")
                #web.debug("SorterFactory:   pathInfo = %s" % pathInfo)
                #web.debug("SorterFactory:   queryResult = %r" % queryResult.get("response"))
                for response in queryResult.get("response"):
                    for thing in response[key]:
                        if "urn:ccss:entity_type:grade_level" in thing["props"]["urn:lri:property_type:types"]:
                            return CcidSorter(key)

                #if "urn:ccss:entity_type:grade_level" in queryResult.get("response")[0][key][0]["props"]["urn:lri:property_type:types"]:
                #    return CcidSorter(key)
            sorter = PathSorter(key)
        elif pathInfo in ["/initiatives", "/frameworks", "/sets",
                          "/competency_containers", "/competencys"]:
            sorter = CcidSorter(key)
        elif pathInfo == "/domains":
            sorter = DomainSorter(key, queryResult)
        elif pathInfo == "/clusters":
            sorter = ClusterSorter(key, queryResult)
        elif pathInfo == "/standards":
            sorter = StandardSorter(key, queryResult)
        elif pathInfo == "/standard_components":
            sorter = ComponentSorter(key, queryResult)
        elif pathInfo == "/anchor_standard_sections":
            sorter = SectionSorter(key, queryResult)
        elif pathInfo == "/anchor_standards":
            sorter = AnchorSorter(key, queryResult)
        elif pathInfo.find("/property_names") != -1:
            sorter = PropertySorter()

        return sorter

class Sorter(object):
    def __init__(self, key, queryResult=None):
        self.key = ""
        self.sorter_type = "Sorter"

    def sort(self, queryResult=None):
        pass

class NameSorter(Sorter):
    """Sorts subjects in QueryResult alphabetically by name"""

    def __init__(self, key, queryResult=None):
        self.key = key
        self.sorter_type = "NameSorter"

    def sortByName(self, item):
        """Sorts by urn:lri:property_type:name."""

        name = item["props"]["urn:lri:property_type:name"]
        return name

    def sort(self, queryResult=None):
        """Sorts QueryResult"""

        for response in queryResult.get("response"):
            sortedItems = sorted(response[self.key], key=self.sortByName)
            response[self.key] = sortedItems

        return queryResult

class PathSorter(Sorter):
    """Sorts query results by previous property on path_step."""

    def __init__(self, key, queryResult=None):
        self.key = key
        self.sorter_type = "PathSorter"

    def isPathQuery(self, request):
        """Tests if request dict is from competency_path query"""

        if not isinstance(request, dict):
            raise WrongTypeError("PathSorter.isPathQuery: argument \"request\": expected dict, got %s" % (type(request)))

        for item in request["response"]:
            status_list = ["urn:lri:entity_type:competency_path" in x["props"]["urn:lri:property_type:types"] for x in item[self.key]]

        return not False in status_list

    def sortByPrevious(self, step_list):
        """Sorts list of path_steps by previous property"""

        prev = "urn:lri:property_type:previous"
        iden = "urn:lri:property_type:id"

        if len(step_list) < 1:
            return step_list

        if not isinstance(step_list[0], dict):
            return []

        # Find first path_step
        # Some path_steps do not have a previous link signifying they are the 
        # first steps
        # Other path_steps have a previous link that point to another path 
        # signifying they are the first steps
        ordered_list = []
        for step in step_list:
            if not step["props"].has_key(prev):
                ordered_list.append(step)
        
        if len(ordered_list) == 0:
            domain = None
            for step in step_list:
                for competency in step["props"]["urn:lri:property_type:competency_in_path"]:
                    if "urn:lri:entity_type:domain" in competency["props"]["urn:lri:property_type:types"]:
                        domain = competency["props"]["urn:ccss:property_type:ccid"]

            for step in step_list:
                previous = step["props"]["urn:lri:property_type:previous"]
                name = step["props"]["urn:lri:property_type:name"]
                if previous.find(domain) == -1:
                    ordered_list.append(step)

        # Order remaining path_steps
        # Compare previous of each item in step_list with front of ordered_list
        for stepi in step_list:
            for stepj in step_list:
                if stepj["props"].has_key(prev):
                    if stepj["props"][prev] == ordered_list[len(ordered_list)-1]["props"][iden]:
                        if stepj not in ordered_list:
                            ordered_list.append(stepj)
                    

        return ordered_list

    def sortPaths(self, queryResult):
        """Sorts competency_paths. --request is a dict w/key 'response'--"""
        print("PathSorter.sortPaths")

        #if not isinstance(queryResult, QueryResult):
        #    raise WrongTypeError("PathSorter.sortPathRequest: argument \"queryResult\": expected QueryResult, got %s" % type(request))

        if not self.isPathQuery(queryResult.getData()):
            return []

        for response in queryResult.get("response"):

            # Sort steps in paths
            for item in response[self.key]: # grade_level, competency_path

                # Extract each path_step list
                step_list = []
                if "urn:lri:property_type:path_step" in item["props"]:
                    step_list = item["props"]["urn:lri:property_type:path_step"]
                if len(step_list) < 1:
                    continue

                # Sort steps
                sorted_steps = self.sortByPrevious(step_list)

                item["props"]["urn:lri:property_type:path_step"] = sorted_steps

                # Some queries have nested path_step lists
                if item["props"].has_key("urn:lri:property_type:path_step"):
                    for step in item["props"]["urn:lri:property_type:path_step"]:
                        if step["props"].has_key("urn:lri:property_type:competency_in_path"):
                            for competency in step["props"]["urn:lri:property_type:competency_in_path"]:
                                if competency["props"].has_key("urn:lri:property_type:path_step"):
                                    nested_step_list = competency["props"]["urn:lri:property_type:path_step"]
                                    nested_sorted_steps = self.sort_by_previous(nested_step_list)
                                    competency["props"]["urn:lri:property_type:path_step"] = nested_sorted_steps
                    
        
            # Sort paths by name
            sorted_names = []
            try:
                for item in response[self.key]:
                    if "urn:lri:property_type:name" not in item["props"]:
                        name = item["props"]["urn:lri:property_type:id"].split(":")[-1]
                        item["props"]["urn:lri:property_type:name"] = name
                        print("PathSorter.sortPaths: Forced name to %s: %s" % (item["props"]["urn:lri:property_type:id"], name))

                print("PathSorter.sortPaths: (%s, %s)" % (response[self.key][0]["props"]["urn:lri:property_type:id"],
                                                          response[self.key][-1]["props"]["urn:lri:property_type:id"]))
                print("PathSorter.sortPaths: sorting ...")
                sorted_names = sorted(response[self.key], key=lambda path: path["props"]["urn:lri:property_type:name"])
                print("PathSorter.sortPaths: ... sorted")
                print("PathSorter.sortPaths: (%s, %s)" % (sorted_names[0]["props"]["urn:lri:property_type:id"],
                                                          sorted_names[-1]["props"]["urn:lri:property_type:id"]))
            except KeyError, e:
                print("PathSorter.sortPaths: ERROR: %r" % e)
                for item in response[self.key]:
                    if "urn:lri:property_type:name" not in item["props"]:
                        print("PathSorter.sortPaths: Path: %s does not have prop: %s" % (item["props"]["urn:lri:property_type:id"],
                                                                                         "urn:lri:property_type:name"))
                return queryResult

            response[self.key] = sorted_names

        return queryResult

    def sort(self, queryResult):
        # Sort each path by path_step
        queryResult = self.sortPaths(queryResult)

        return queryResult

class CcidSorter(Sorter):
    """Sorts type in QueryResult numerically by CCID"""

    def __init__(self, key, queryResult=None):
        self.key = key
        self.sorter_type = "CcidSorter"

    def sortByCcid(self, item):
        """Natural sorts by urn:ccss:property_type:ccid.
        See http://www.codinghorror.com/blog/archives/001018.html

"""
        uid = ""
        try:
            if "urn:ccss:property_type:ccid" in item["props"]:
                uid = item["props"]["urn:ccss:property_type:ccid"]
            else:
                uid = item["props"]["urn:lri:property_type:id"]
        except TypeError, e:
            print("CcidSorter.sortByCcid: Caught TypeError")
            print("CcidSorter.sortByCcid: item = %r" % item)

        return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', uid)]

    def sort(self, queryResult=None):
        for response in queryResult.getData()["response"]:
            sortedItems = sorted(response[self.key], key=self.sortByCcid)
            response[self.key] = sortedItems

        return queryResult

class DomainSorter(CcidSorter):
    """Sorts domains in QueryResult numerically by CCID"""

    def sort(self, queryResult=None):
        """Sorts domains"""
        return CcidSorter.sort(self, queryResult)

class ClusterSorter(CcidSorter):
    """Sorts clusters in QueryResult numerically by CCID"""

    def sort(self, queryResult=None):
        """Sorts clusters"""
        return CcidSorter.sort(self, queryResult)

class StandardSorter(CcidSorter):
    """Sorts standards in QueryResult by CCID"""

    def __init__(self, key, queryResult):
        self.sortEla = False
        CcidSorter.__init__(self, key, queryResult)

    def sort(self, queryResult=None):
        """Sorts standards"""
        return CcidSorter.sort(self, queryResult)


class ComponentSorter(CcidSorter):
    """Sorts standard_components by CCID"""

    def sort(self, queryResult=None):
        """Sorts standard_components"""
        return CcidSorter.sort(self, queryResult)

class SectionSorter(CcidSorter):
    """Sorts anchor_standard_sections by CCID"""

    def sort(self, queryResult=None):
        """Sorts and flattens sections"""
        return CcidSorter.sort(self, queryResult)

class AnchorSorter(CcidSorter):
    """Sorts anchor_standards by CCID"""

    def sort(self, queryResult=None):
        """Sorts and flattens anchor_standards"""
        return CcidSorter.sort(self, queryResult)
             
class ResourceSorter(object):
    def __init__(self, queryResult):
        raise NotImplementedError("ResourceSorter is not implemented")

class StrandSorter(object):
    def __init__(self, queryResult):
        raise NotImplementedError("StrandSorter is not implemented")

class PropertySorter(object):
    def __init__(self):
        pass

    def sort(self, queryResult):
        queryResult.get("response")[0]["property_names"] = sorted(queryResult.getPropertyNames())
        return queryResult
            
class FilterSorter(Sorter):
    def __init__(self, key, sortBy, queryResult=None):
        self.key = key
        self.sortBy = sortBy
        self.sorter_type = "FilterSorter"

    def sortByProp(self, item):
        """Natural sorts by self.sortBy.
        See http://www.codinghorror.com/blog/archives/001018.html

"""
        prop = item["props"][self.sortBy]
        return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', prop)]

    def sort(self, queryResult=None):
        """Sorts QueryResult"""
        print("FilterSorter.sort")

        noProp = "None"
        for response in queryResult.get("response"):
            for item in response[self.key]:
                entityId = item["props"]["urn:lri:property_type:id"]
                if self.sortBy not in item["props"]:
                    item["props"][self.sortBy] = noProp
                    print("FilterSorter.sort: Forced prop: %s of: %s to: %s" % (self.sortBy, entityId, noProp))

        for response in queryResult.get("response"):
            sortedItems = sorted(response[self.key], key=self.sortByProp)
            response[self.key] = sortedItems

        return queryResult

