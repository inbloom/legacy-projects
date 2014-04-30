import json

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

class HttpConfig(object):
    def __init__(self, documentRoot, configFile="http_config.json"):
        self._documentRoot = documentRoot
        self._configFile = configFile

        self.configDir = "%s/config" % documentRoot
        self.configFile = configFile
        self.config = self.load()

    def __repr__(self):
        return "<HttpConfig('%s, %s')>" % (self._documentRoot, self._configFile)

    def __str__(self):
        return "configDir: %s, configFile: %s, config: %r" % (self.configDir,
                                                              self.configFile,
                                                              self.config)

    def load(self):
        config = json.load(open("%s/%s" % (self.configDir, self.configFile)))
        return config

    
