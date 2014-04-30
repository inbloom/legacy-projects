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
# Format
###############################################################################

import json

class FormatterFactory(object):
    def CreateFormatter(self, toFormat):
        formatter = None
        if toFormat == "json":
            formatter = JsonFormatter()
        elif toFormat in ["xml", "johnxml", "oldxml"]:
            formatter = XmlFormatter(which=toFormat)
        elif toFormat == "yaml":
            formatter = YamlFormatter()
        else:
            formatter = JsonFormatter()

        return formatter

class JsonFormatter(object):
    """Converts to JSON"""

    def format(self, content):
        content = json.dumps(content, indent=3, sort_keys=True)
        return content

class XmlFormatter(object):
    """Converts to XML"""

    def __init__(self, which="xml"):
        self.which = which

    def format(self, content):
        """Formats content as XML"""

        if self.which == "xml":
            content = self.renderXml(content).encode("utf-8")
        elif self.which == "johnxml":
            content = self.renderJohnXml(content).encode("utf-8")
        elif self.which == "oldxml":
            content = self.renderOldXml(content).encode("utf-8")

        return content

    def renderXml(self, x, indent="", tagname="", depth=0):
        """Recursively converts to XML"""

        s=[]

        first = False
        if indent == "":
            first = True

        if first:
            s.append("<?xml version=\"1.0\" ?>\n\n<root>\n")
            indent="  "

        if isinstance(x,list):
            for y in x:
                if isinstance(y,list) or isinstance(y,dict):
                    s.append(indent+"<value>\n")
                    s.append("%s" % (self.renderXml(y,indent=indent+"  ",depth=depth+1)))
                    s.append(indent+"</value>\n")
                else:
                    try:
                        s.append(indent+"<value>%s</value>\n" % (str(y)))
                    except:
                        s.append(indent+"<value>%s</value>\n" % (repr(y)))

        elif isinstance(x,dict):
            for k,v in x.items():
                s.append(indent+"<pair>\n")
                s.append(indent+"  <key>%s</key>\n" % (k))
                if not isinstance(v,list):
                    v=[v]
                s.append(self.renderXml(v,indent=indent+"  ",depth=depth+1))
                s.append(indent+"</pair>\n")

        if first:
            s.append("</root>")

        return("".join(s))

    def renderJohnXml(self, x, indent="", tagname="", depth=0):
        s=[]

        first = False
        if indent == "":
            first = True

        if first:
            s.append("<?xml version=\"1.0\" ?>\n\n<root>\n")
            indent="  "

        if isinstance(x,list):
            for y in x:
                if isinstance(y,list) or isinstance(y,dict):
                    s.append(indent+"<value>\n")
                    s.append("%s" % (self.renderJohnXml(y,indent=indent+"  ",depth=depth+1)))
                    s.append(indent+"</value>\n")
                else:
                    try:
                        s.append(indent+"<value>%s</value>\n" % (str(y)))
                    except:
                        s.append(indent+"<value>%s</value>\n" % (repr(y)))
        elif isinstance(x,dict):
            for k,v in x.items():
                s.append(indent+"<pair key=\"%s\">\n" % (k))
                if not isinstance(v,list):
                    v=[v]
                s.append(self.renderJohnXml(v,indent=indent+"  ",depth=depth+1))
                s.append(indent+"</pair>\n")

        if first:
            s.append("</root>")

        return("".join(s))

    def mangleTag(self, t):
        return t.replace(":","").replace("/","_")

    def renderOldXml(self, x, indent="", tagname="", depth=0):
        s=[]

        first = False
        if indent == "":
            first = True

        if first:
            s.append("<?xml version=\"1.0\" ?>\n\n<root>\n")
            indent="    "

        tagname = self.mangleTag(tagname)

        if isinstance(x,list):
            for i in x:
                if isinstance(i,list) or isinstance(i,dict):
                    s.append(indent+'<'+tagname+'>'+"\n"+indent+"    "+self.renderOldXml(i,indent=indent+"    ",depth=depth+1).strip()+"\n"+indent+'</'+tagname+">\n")
                else:
                    s.append(indent+'<'+tagname+'>'+self.renderOldXml(i,indent=indent+"    ",depth=depth+1).strip()+'</'+tagname+">\n")
        elif isinstance(x,dict):
            for k,v in x.items():

                k = self.mangleTag(str(k))

                if isinstance(v,list):
                    s.append(self.renderOldXml(v,indent=indent+"    ",tagname=k,depth=depth+1))
                elif isinstance(v,dict):
                    s.append(indent+"<"+str(k)+">") # open tag
                    s.append("\n"+self.renderOldXml(v,indent=indent+"    ",depth=depth+1)+indent)
                    s.append('</'+str(k)+">\n") # close tag
                else:
                    s.append(indent+"<"+str(k)+">") # open tag
                    try:
                        s.append(v.strip())
                    except:
                        s.append(str(v).strip())
                    s.append('</'+str(k)+">\n") # close tag
        else:
            s.append(indent+str(x).strip()+"\n")

        if first:
            s.append("</root>")

        return("".join(s))

class YamlFormatter(object):
    def __init__(self):
        raise NotImplementedError("YamlFormatter is not implemented")

    def sort(self, content):
        return content
