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

"""Web app for building competency_path"""

import requests
import sys
import web

from pathbuilder import form

render = web.template.render("/var/www/apps-test/pathbuilder/templates")
#urls = ("", "Builder",
#        "/", "Builder",
#        "/initiatives/(.*)", "Initiatives",
#        "/frameworks/(.*)", "Frameworks",
#        "/sets/(.*)", "Sets",
#        "/grade_levels/(.*)", "GradeLevels",
#        "/domains/(.*)", "Domains")
urls = ("", "Builder",
        "/", "Builder")
app = web.application(urls, globals())
application = app.wsgifunc()

PROPERTIES = ["urn:lri:property_type:name",
              "urn:ccss:property_type:ccid"]

def getEntities(name, filters=[], parent={}):
    url = "http://knowledgeweb.appliedminds.com:9000/ccss/%s" % name
    url += "?"
    if len(parent) > 0:
        if "name" in parent:
            url += "%s=%s&" % (parent["name"], parent["id"])
    url += "property=%s" % filters[0]
    for f in filters[1:]:
        url += "&property=%s" % f
    web.debug("getEntities: url = %s" % url)
    response = requests.get(url)
    return response.text

class Initiatives(object):
    def GET(self, name=None):
        return getEntities("initiatives", filters=PROPERTIES)

class Frameworks(object):
    """
Both: Framework contained_by initiative
Math: Framework contains set
ELA: Framework contains domain

"""
    def GET(self, parentId=None):
        name = "frameworks"
        parent = {"name": "initiative", "id": parentId}
        return getEntities(name, filters=PROPERTIES, parent=parent)

class Sets(object):
    """
Math: Set contained_by framework
Math: Set contains grade_level

"""
    def GET(self, parentId=None):
        name = "sets"
        parent = {"name": "framework", "id": parentId}
        return getEntities(name, filters=PROPERTIES, parent=parent)

class GradeLevels(object):
    """
Math: Grade_level contained_by set
Math: Grade_level contains domain
ELA: Grade_level contained_by domain
ELA: Grade_level contains standard

"""

    def GET(self, parentId=None):
        name = "frameworks"
        parent = {"name": "set", "id": initiative}
        return getEntities(name, filters=PROPERTIES, parent=parent)

class Domains(object):
    """
Math: Domain contained_by grade_level
Math: Domain contains cluster

"""
    def GET(self, framework=None):
        name = "domains"
        # XXX
        if framework == "urn:ccss:framework:CCSS.ELA-Literacy":
            name = "grade_levels"
        parent = {"name": "framework", "id": framework}
        return getEntities(name, filters=PROPERTIES, parent=parent)

class Standards(object):
    """
Math: Standard contained_by domain
ELA: Standard contained_by grade_level

"""
    def GET(self, domain=None):
        name = "standards"
        parent = {"name": "domain", "id": domain}
        return getEntities(name, filters=Properties, parent=parent)
        
class Builder(object):
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")

        builderForm = form.Form()
        return render.form(builderForm.form())

    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")

        builderForm = form.Form()
        if not builderForm.form().validates():
            return render.form(builderForm.form())

        ret = ""
        try:
            serverhost = "knowledgeweb.appliedminds.com"
            serverport = 9000

            app = "/ccss"
            action = "/create"
            #if "action" in userData:
            #    action = userData["action"]

            userData = web.input()
            web.debug(userData)
            entityType = "competency_path"

            # Post some data to /ccss/
            web.header("Content-Type", "xml")
            url = "http://%s:%d%s/%s%s" % (serverhost, serverport, app, entityType, action)
            web.debug(url)

            response = requests.post(url, data=userData)
            ret = response.text
            web.debug(ret)

        except urllib2.URLError, e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            msg += "URLError: url: " + url + ": error: " + str(e) + "\n"
            msg += "reason: " + e.reason + "\n"
            msg += "-" * 60 + "\n"
            msg += traceback.format_exc()
            msg += "-" * 60 + "\n"

        except urllib2.HTTPError, e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            msg += "HTTPError: url: " + url + ": error: " + str(e) + "\n"
            msg += "-" * 60 + "\n"
            msg += traceback.format_exc()
            msg += "-" * 60 + "\n"

        return ret
