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

"""Web app for creating an entity in LRI"""

import os.path
import requests
import sys
import traceback
import urllib2
import web
from web import form

web.config.debug = True

render = web.template.render("/var/www/apps-test/ccss_create/templates/")

urls = ("", "Create",
        "/", "Create",
        "/templates", "Template",
        "/template/", "Template",
        "/template/(.*)/(.*)", "Template")
web.debug(urls)

app = web.application(urls, globals())
application = app.wsgifunc()

# Form elems
defaultFormat = "Pick a data format"
jsonFormats = ["json"]
xmlFormats = ["xml", "johnxml", "oldxml"]
formats = [defaultFormat] + jsonFormats + [xmlFormats[0]]

defaultType = "Pick a CCSS type"
ccssTypes = ["initiative",
             "framework",
             "set",
             "grade_level",
             "competency",
             "competency_container",
             "competency_path", 
             "learning_resource"
             ]
types = [defaultType] + ccssTypes

defaultData = "Enter CCSS data here"
CreateForm = form.Form(
    form.Dropdown("type", sorted(types), value=defaultType, id="types"),
    form.Dropdown("format", sorted(formats), value=defaultFormat, id="formats"),
    form.Textarea("data", rows=30, cols=90, value=defaultData, id="data"))

class Template(object):
    def __init__(self):
        web.debug("Template.__init__")
        self.data = self.loadTemplates("%s/ccss/templates" % web.ctx.env["DOCUMENT_ROOT"])
        web.debug("Template.__init__: data = %r" % self.data)

    def loadTemplate(self, path):
        fd = open(path)
        lines = fd.readlines()
        fd.close()
        return "".join(lines)

    def loadTemplates(self, templatesDir):
        data = {}
        for t in ccssTypes:
            data[t] = {}
            for f in formats[1:]:
                path = "%s/%s.%s" % (templatesDir, t, f)
                data[t][f] = "Template file not found: %s" % path
                if not os.path.exists(path):
                    continue
                data[t][f] = self.loadTemplate(path)

        return data

    def GET(self, typeIn=None, formatIn=None):
        web.debug("Template.GET");
        web.debug("Template.GET: typeIn = %s" % typeIn)
        web.debug("Template.GET: formatIn = %s" % formatIn)

        data = ""
        try:
            data = self.data[typeIn][formatIn]
        except KeyError, e:
            web.debug(e)
        web.debug(data)

        web.header("Content-Type", "text/%s; charset=utf-8" % formatIn)
        web.header("Access-Control-Allow-Origin", "*")
        return data

class Create(object):
    def GET(self, name=None):
        web.debug("Create.GET")

        createForm = CreateForm()
        return render.form(createForm)

    def POST(self, name=None):
        web.debug("Create.POST")

        createForm = CreateForm()
        if not createForm.validates():
            return render.form(createForm)

        web.debug("data: %s" % web.data())

        msg = "ccss_create\n\n"
        ret = ""
        try:
            serverhost = "knowledgeweb.appliedminds.com"
            serverport = 9000

            app = "/ccss"
            action = "/create"

            userData = web.input()
            web.debug(userData)
            ccssType = userData["type"]

            # Post some data to /ccss/
            web.header("Content-Type", userData.type)
            url = "http://%s:%d%s/%s%s" % (serverhost, serverport, app, ccssType, action)
            web.debug("url = %s\n" % url)
            response = requests.post(url, data=userData)

            msg += "\nusing requests: \n"
            msg += "status code: " + str(response.status_code) + "\n"
            msg += "headers: \n"
            for h in response.headers:
                msg += "    " + h + ": " + response.headers[h] + "\n"
            msg += "encoding: " + str(response.encoding) + "\n"

            msg += "\nresponse text: \n"
            msg += response.text + "\n"

            msg += "\nresponse content: \n"
            msg += response.content + "\n"

            if response.json is not None:
                msg += "\nresponse.json: \n"
                msg += str(response.json) + "\n"

            ret = response.text

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

        web.debug(msg)
        return ret
