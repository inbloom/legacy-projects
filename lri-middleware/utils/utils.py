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

import json

def getJson(response):
    """Safely get json results from requests response"""

    result = None
    try:
        result = json.loads(response.content)
    except AttributeError, e:
        print("no content",e)

        try:
            result = response.json()
        except TypeError, e:
            print("no json()",e)

            try:
                result = r.json
            except AttributeError, e:
                print("no json",e)

    if result is None:
        raise Exception("Could not get JSON from requests response")

    return result

def getText(response):
    """Safely get text results from requests response"""

    result = None
    try:
        result = response.content
    except AttributeError, e:
        print("getText: No content")

        try:
            result = response.text
        except AttributeError, e:
            print("getText: No text")

    if result is None:
        raise Exception("Could not get text from requests response")

    return result

