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

import web
from web import form as webform

import httpconfig

class Form(object):
    """Form class"""

    def __init__(self, names=[]):
        self._form = self.createForm(names)
        self.httpConfig = httpconfig.HttpConfig(web.ctx.env["DOCUMENT_ROOT"])

    @property
    def form(self):
        return self._form

    def createForm(self, names=[]):

        # Text area for sending path data
        pathDataArea = webform.Textarea("", rows=30, cols=90, value="", id="pathData", hidden=True)

        form = webform.Form(pathDataArea)

        return form
