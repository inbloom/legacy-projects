#!/usr/bin/env python
# Copyright 2012-2013 inBloom, Inc. and its affiliates.
#
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
import json,yaml,traceback,sys,re
from bs4 import BeautifulSoup

math_grades = ['K','1','2','3','4','5','6','7','8','HSN','HSA','HSF','HSG','HSS']
ela_grades = ['K','1','2','3','4','5','6','7','8','6-8','9-10','11-12']



# Conveniences function to get the data structs

def ccss_data():
    lridir = "."
    cx = ccss_xml(mathfilename=lridir+"/external_schema/Math.xml",
                  elafilename=lridir+"/external_schema/ELA-Literacy.xml",
                  outfilename=lridir+"/test_suites/load")
    return cx

def make_ccss_id(object_type,dot_id):
    return "urn:ccss:%s:%s" % (object_type,dot_id)

def name_from_description(d,numwords):
    return ' '.join(d.split(' ')[0:numwords])+'...'

def parse_uri_id(uri_id):

    dot_id = uri_id.replace('http://corestandards.org','CCSS').replace('/','.')
    i = dot_id.split('.')

    # Wrangling because we have multiple forms of punctuation as separators and we
    # want them all to be "."
    #i=dot_id.replace('ELA-Literacy','QQqqQQ')
    #i=i.replace('6-8','TTttTT')
    #i=i.replace('9-10','RRrrRR')
    #i=i.replace('11-12','SSssSS')
    #i=i.replace('-','.')
    #i=i.replace('QQqqQQ','ELA-Literacy')
    #i=i.replace('TTttTT','6-8')
    #i=i.replace('RRrrRR','9-10')
    #i=i.replace('SSssSS','11-12')
    #i=i.split('.')

    # Our parsed data structure
    r={}

    # Setup to capture all forms of IDs
    r['dot_id'] = dot_id
    p = {}
    r['paths'] = p
    dotpath = ''

    r['initiative'] =  i[0]
    dotpath = i[0]
    p['initiative'] = dotpath
    r['framework'] =  i[1]
    dotpath += '.'+i[1]
    p['framework'] =  dotpath


    if r['framework'] == 'Math':
        r['set'] =  i[2]
        dotpath += '.'+i[2]
        p['set'] = dotpath
        dotpath += '.'+i[3]
        if r['set'] == 'Practice':
            r['standard'] =  i[3]
            p['standard'] = dotpath
            r['object_type'] = 'practice_standard'
            return r
        elif r['set'] == 'Content':
            if len(i) == 4:
                if i[3] not in math_grades:
                    # Is under-defined "CCSS.Math.Content.*" format
                    r['domain'] = i[3]
                    p['domain'] = dotpath
                    r['object_type'] = 'undef_domain'
                    return r
                else:
                    # Is grade level.
                    r['grade'] = i[3]
                    p['grade'] = dotpath
                    r['object_type'] = 'grade'
                    return r 
            r['grade'] =  i[3]
            p['grade'] = dotpath
            dotpath += '.'+i[4]
            r['domain'] =  i[4]
            p['domain'] = dotpath
            if len(i) == 5:
                r['object_type'] = 'domain'
                return r
            # We have to wrangle this due to missing . in dot_id notation after cluster
            i[5] = re.sub('(\d{1,2}.*)','.\\1',i[5])
            tail = i[5].split('.')
            if len(tail) > 1:
                i[5] = tail[0]
                if len(i) == 6:
                    i.append(tail[1])
                else:
                    i[6] = tail[1]
                r['dot_id'] = '.'.join(i)

            dotpath += '.'+i[5]
            r['cluster'] = i[5]
            p['cluster'] = dotpath
            if len(i) == 6:
                r['object_type'] = 'cluster'
                return r

            # We have to wrangle this due to missing . in dot_id notation after standard
            i[6] = re.sub('([a-z])','.\\1',i[6])
            tail = i[6].split('.')
            if len(tail) > 1:
                i[6] = tail[0]
                i.append(tail[1])
                r['dot_id'] = '.'.join(i)

            dotpath += '.'+i[6]
            r['standard'] =  i[6]
            p['standard'] = dotpath
            if len(i) == 7:
                r['object_type'] = 'standard'
                return r
            dotpath += '.'+i[7]
            r['component'] =  i[7]
            p['component'] = dotpath
            r['object_type'] = 'component'
            return r
    elif r['framework'] == 'ELA-Literacy':
        dotpath += '.'+i[2]
        if i[3] not in ela_grades:
            # Must include 'set' field -- onlt CCRA for now, so is chanor standard
            p['set'] = dotpath
            r['set'] = i[2]
            dotpath += '.'+i[3]
            r['strand'] = i[3]
            p['strand'] = dotpath
            dotpath += '.'+i[4]
            r['standard'] = i[4]
            p['standard'] = dotpath
            r['object_type'] = 'anchor_standard'
            return r
        r['strand_domain'] = i[2]
        p['strand_domain'] = dotpath
        dotpath += '.'+i[3]
        r['grade'] = i[3]
        p['grade'] = dotpath
        if len(i) == 4:
            r['object_type'] = 'grade'
            return r

        # We have to wrangle this due to missing . in dot_id notation after standard
        i[4] = re.sub('([a-z])','.\\1',i[4])
        tail = i[4].split('.')
        if len(tail) > 1:
            i[4] = tail[0]
            i.append(tail[1])
            r['dot_id'] = '.'.join(i)


        r['standard'] = i[4]
        dotpath += '.'+i[4]
        p['standard'] = dotpath
        if len(i) == 5:
            r['object_type'] = 'standard'
            return r
        dotpath += '.'+i[5]
        r['component'] = i[5]
        p['component'] = dotpath
        r['object_type'] = 'component'
        return r
    else:
        print "BAD FRAMEWORK FOR ID:",r
        return None




class ccss_xml(object):
  
    def __init__(self,mathfilename=None,elafilename=None,outfilename=None):
        self.mathfilename = mathfilename
        self.elafilename = elafilename
        self.outfilename = outfilename
        self.m = {}
        self.e = {}
        self.guids = {}
        self.dot_ids = {}
        self.dupes = {}
        self.missing_dot_id = []
        self.bad_record = []
        self.initiative = {}
        self.framework = {}
        self.set = {}
        self.grade = {}
        self.strand = {}
        self.domain = {}
        self.anchor = {}
        self.anchsect = {}
        self.cluster = {}
        self.standard = {}
        self.component = {}
        self.shortname_word_count = 3

        self.load_xml()

    def load_xml(self):

        self.m_lsis = BeautifulSoup(open(self.mathfilename).read()).findAll("learningstandarditem")
        print "Math LSI count =",len(self.m_lsis)
        self.e_lsis = BeautifulSoup(open(self.elafilename).read()).findAll("learningstandarditem")
        print "ELA LSI count =",len(self.e_lsis)


    def parse_lsis(self,lsi_list,dest):
        dupe_count = 0
        for lsi in lsi_list:
            i = self.parse_learning_standard_item(lsi)

            valid_record = 'good'
            if not i['raw_dot_id']:
                self.missing_dot_id.append(i)
                valid_record = 'bad'
                continue

            if not i['guid_id']:
                self.missing_dot_id.append(i)
                valid_record = 'bad'

            if i['uri_id'] in dest:
                self.dupes[i['uri_id']] = [i,dest[i['uri_id']]]
                #print "URI ID DUPE:",json.dumps(i,indent=4),json.dumps(dest[i['uri_id']],indent=4)
                #del dest[i['uri_id']]
                dupe_count += 1

            if i['guid_id'] in self.guids:
                #print i,self.guids[i['guid_id']]
                self.dupes[i['guid_id']] = [i,self.guids[i['guid_id']]]
                #print "GUID ID DUPE:",json.dumps(i,indent=4),json.dumps(i['uri_id'],indent=4)
                #del self.guids[i['uri_id']]
                dupe_count += 1
            else:
                self.guids[i['guid_id']] = i

            if valid_record and i['raw_dot_id'] in self.dot_ids:
                self.dupes[i['raw_dot_id']] = [i,self.guids[i['raw_dot_id']]]
                #print "DOT ID DUPE:",json.dumps(i,indent=4),json.dumps(i['uri_id'],indent=4)
                #del self.dot_ids[i['uri_id']]
                dupe_count += 1
            else:
                self.dot_ids[i['raw_dot_id']] = i

            if valid_record:
                dest[i['raw_dot_id']] = i

        print "TOTAL DUPES =",dupe_count

    def parse(self):
        self.parse_lsis(self.m_lsis,self.m)
        self.parse_lsis(self.e_lsis,self.e)


    def parse_learning_standard_item(self,lsi):
        rec = {'errors':[]}

        rec['uri_id'] = lsi.find('refuri').text
        rec['raw_dot_id'] = lsi.find('statementcode').text
        rec['guid_id'] = lsi.find('learningstandarddocumentrefid').text
        try:
            rec['parent_guid'] = lsi.find('learningstandarditemrefid').text
        except:
            pass
        rec['grades'] = [ g.text for g in lsi.findAll('gradelevel') ]
        rec['type'] = lsi.find('description').text
        rec['type_number'] = lsi.find('number').text
        rec['text'] = lsi.find('statement').text

        if rec['uri_id'] and not rec['raw_dot_id']:
            rec['errors'].append('Missing CCSS dot ID')

        if rec['raw_dot_id']:
            #try:
                rec['parsed_id'] = parse_uri_id(rec['uri_id'])
            #except:
            #    print "BAD DOT ID:",json.dumps(rec,indent=4)
            #    print traceback.format_exc()
            #    self.bad_record.append(rec)
        return rec


    def process_math(self):

        raw_dot_ids = self.m.keys()
        raw_dot_ids.sort()  # So standars come before components

        raw_by_cooked = dict([(i['parsed_id']['dot_id'],i['raw_dot_id']) for i in self.m.values()])
        dot_ids = raw_by_cooked.keys()
        dot_ids.sort()
        
        for dot_id in dot_ids:
            rec = self.m[raw_by_cooked[dot_id]]
            r = rec['parsed_id']
            print "PROCESSING:",raw_by_cooked[dot_id],r['dot_id']

            iid = r["paths"]["initiative"]
            fid = r["paths"]["framework"]
            seid =r["paths"]["set"]
            sid = r["paths"]["standard"]


            if iid not in self.initiative:
                     self.initiative[iid] =  \
                        { "urn:lri:property_type:id":make_ccss_id('initiative',iid),
                          "urn:ccss:property_type:ccid":iid,
                          "urn:lri:property_type:name":"Initiative %s" % (iid),
                          "urn:lri:property_type:contains":[],
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:initiative"]}

            if fid not in self.framework:
                self.framework[fid] =  \
                        { "urn:lri:property_type:id":make_ccss_id('framework',fid),
                          "urn:ccss:property_type:ccid":fid,
                          "urn:lri:property_type:contains":[],
                          "urn:lri:property_type:name":"Framework %s %s" % (iid, fid),
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:framework"]}
            self.initiative[iid]["urn:lri:property_type:contains"].append(make_ccss_id('framework',fid))

            if seid not in self.set:
                self.set[seid] =  \
                        { "urn:lri:property_type:id":make_ccss_id('set',seid),
                          "urn:ccss:property_type:ccid":seid,
                          "urn:lri:property_type:contains":[],
                          "urn:lri:property_type:name":"Set %s" % (seid),
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:set"]}
            self.framework[fid]["urn:lri:property_type:contains"].append(make_ccss_id('set',seid))

            if r['set'] == 'Practice':

                self.standard[sid] =  \
                    { "urn:lri:property_type:id":make_ccss_id('standard',sid),
                      "urn:ccss:property_type:ccid":sid,
                      "urn:lri:property_type:description":rec['text'],
                      "urn:lri:property_type:name":name_from_description(rec['text'],numwords=self.shortname_word_count),
                      "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                        "urn:lri:entity_type:competency", 
                                                        "urn:lri:entity_type:competency_container", 
                                                        "urn:lri:entity_type:learning_objective",
                                                        "urn:ccss:entity_type:practice_standard"]}
                self.set[seid]["urn:lri:property_type:contains"].append(make_ccss_id('standard',sid))
                    
                
            elif r['set'] == 'Content':
                 
                gid = r["paths"]["grade"]
                did = r["paths"]["domain"]
                clid = r["paths"]["cluster"]

                if gid not in self.grade:
                    self.grade[gid] =  \
                        { "urn:lri:property_type:id":make_ccss_id('grade',gid),
                          "urn:ccss:property_type:ccid":gid,
                          "urn:lri:property_type:contains":[],
                          "urn:lri:property_type:name":"Math Grade %s" % (gid),
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:grade_level"]}
                self.set[seid]["urn:lri:property_type:contains"].append(make_ccss_id('grade',gid))

                if did not in self.domain:
                    self.domain[did] =  \
                        { "urn:lri:property_type:id":make_ccss_id('domain',did),
                          "urn:ccss:property_type:ccid":did,
                          "urn:lri:property_type:contains":[],
                          "urn:lri:property_type:name":"Math Domain %s" % (did),
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:domain"]}
                self.grade[gid]["urn:lri:property_type:contains"].append(make_ccss_id('domain',did))

                if clid not in self.cluster:
                    self.cluster[clid] =  \
                        { "urn:lri:property_type:id":make_ccss_id('cluster',clid),
                          "urn:ccss:property_type:ccid":clid,
                          "urn:lri:property_type:contains":[],
                          "urn:lri:property_type:name":"Math Cluster %s" % (clid),
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:cluster"]}
                self.domain[did]["urn:lri:property_type:contains"].append(make_ccss_id('cluster',clid))

                if r['object_type'] == 'standard':
                    self.standard[sid] =  \
                        { "urn:lri:property_type:id":make_ccss_id('standard',sid),
                          "urn:ccss:property_type:ccid":sid,
                          "urn:lri:property_type:contains":[],
                          "urn:lri:property_type:description":rec['text'],
                          "urn:lri:property_type:name":name_from_description(rec['text'],numwords=self.shortname_word_count),
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:standard"]}
                    self.cluster[clid]["urn:lri:property_type:contains"].append(make_ccss_id('standard',sid))
                    # We add domain too.  A bit of a denormalization, but the IDs themselves are denormalized.
                    self.domain[did]["urn:lri:property_type:contains"].append(make_ccss_id('standard',sid))

                elif r['object_type'] == 'component':
                    coid = r["paths"]["component"]
                    self.component[coid] =  \
                        { "urn:lri:property_type:id":make_ccss_id('standard_component',coid),
                          "urn:ccss:property_type:ccid":r['dot_id'],
                          "urn:lri:property_type:description":rec['text'],
                          "urn:lri:property_type:name":name_from_description(rec['text'],numwords=self.shortname_word_count),
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:standard_component"]}
                    self.standard[sid]["urn:lri:property_type:contains"].append(make_ccss_id('standard_component',coid))

    def process_ela(self):

        raw_dot_ids = self.e.keys()
        raw_dot_ids.sort()  # So standars come before components

        raw_by_cooked = dict([(i['parsed_id']['dot_id'],i['raw_dot_id']) for i in self.e.values()])
        dot_ids = raw_by_cooked.keys()
        dot_ids.sort()
        
        for dot_id in dot_ids:
            rec = self.e[raw_by_cooked[dot_id]]
            r = rec['parsed_id']
            print "PROCESSING:",raw_by_cooked[dot_id],r['dot_id']

            iid = r["paths"]["initiative"]
            fid = r["paths"]["framework"]

            if fid not in self.framework:
                self.framework[fid] =  \
                        { "urn:lri:property_type:id":make_ccss_id('framework',fid),
                          "urn:ccss:property_type:ccid":fid,
                          "urn:lri:property_type:contains":[],
                          "urn:lri:property_type:name":"Framework %s %s" % (iid,fid),
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:framework"]}
            self.initiative[iid]["urn:lri:property_type:contains"].append(make_ccss_id('framework',fid))

            if r['object_type'] == 'anchor_standard':
                # Must be anchor standard
                seid =r["paths"]["set"]
                strid = r["paths"]["strand"]
                anchid = r["paths"]["standard"]
                
                if seid not in self.set:
                    self.set[seid] =  \
                        { "urn:lri:property_type:id":make_ccss_id('set',seid),
                          "urn:ccss:property_type:ccid":seid,
                          "urn:lri:property_type:contains":[],
                          "urn:lri:property_type:name":"Set %s" % (seid),
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:set"]}
                    self.framework[fid]["urn:lri:property_type:contains"].append(make_ccss_id('set',seid))

                if strid not in self.strand: 
                    self.strand[strid] =  \
                        { "urn:lri:property_type:id":make_ccss_id('strand',strid),
                          "urn:ccss:property_type:ccid":strid,
                          "urn:lri:property_type:name":"Strand %s" % (strid),
                          "urn:ccss:property_type:includes_anchor_standard":[],
                          "urn:ccss:property_type:includes_domain":[],
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:strand"]}
                self.set[seid]["urn:lri:property_type:contains"].append(make_ccss_id('strand',strid))

                if anchid not in self.anchor: 
                    self.anchor[anchid] =  \
                        { "urn:lri:property_type:id":make_ccss_id('anchor_standard',anchid),
                          "urn:ccss:property_type:ccid":anchid,
                          "urn:ccss:property_type:anchors":[],
                          "urn:lri:property_type:name":"Anchor Standard %s" %(anchid),
                          "urn:lri:property_type:description":rec['text'],
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:anchor_standard"]}
                self.strand[strid]["urn:ccss:property_type:includes_anchor_standard"].append(make_ccss_id('anchor_standard',anchid))

            elif r['object_type'] in ['standard','component']:
                did = r["paths"]["strand_domain"]
                gid = r["paths"]["grade"]
                sid = r["paths"]["standard"]

                if did not in self.domain:
                    self.domain[did] =  \
                        { "urn:lri:property_type:id":make_ccss_id('domain',did),
                          "urn:ccss:property_type:ccid":did,
                          "urn:lri:property_type:contains":[],
                          "urn:lri:property_type:name":"ELA-Literacy Domain %s" % (did),
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:domain"]}
                self.framework[fid]["urn:lri:property_type:contains"].append(make_ccss_id('domain',did))

                # Bind strands to strand+domain ("domain") objects
                strand_code=None
                if r['strand_domain'] in ['L','W','SL','RF','RI','RL']:
                    if r['strand_domain'].startswith('R'):
                        strand_code="R"
                    else:
                        strand_code=r['strand_domain']
                    strid = 'CCSS.ELA-Literacy.CCRA.'+strand_code
                    self.strand[strid]["urn:ccss:property_type:includes_domain"].append(make_ccss_id('domain',did))
                    # We calculate anchor standard ID so we can related directly to standard
                    anchid = strid+'.'+r["standard"]

                if gid not in self.grade:
                    self.grade[gid] =  \
                        { "urn:lri:property_type:id":make_ccss_id('grade',gid),
                          "urn:ccss:property_type:ccid":gid,
                          "urn:lri:property_type:contains":[],
                          "urn:lri:property_type:name":"ELA-Literacy Grade %s" % (gid),
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:grade_level"]}
                self.domain[did]["urn:lri:property_type:contains"].append(make_ccss_id('grade',gid))

                if r['object_type'] == 'standard':
                    self.standard[sid] =  \
                        { "urn:lri:property_type:id":make_ccss_id('standard',sid),
                          "urn:ccss:property_type:ccid":sid,
                          "urn:lri:property_type:contains":[],
                          "urn:lri:property_type:description":rec['text'],
                          "urn:lri:property_type:name":name_from_description(rec['text'],numwords=self.shortname_word_count),
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:standard"]}
                    self.grade[gid]["urn:lri:property_type:contains"].append(make_ccss_id('standard',sid))
                    if strand_code:
                        self.anchor[anchid]['urn:ccss:property_type:anchors'].append(make_ccss_id('standard',sid))
                    

                elif r['object_type'] == 'component':
                    coid = r["paths"]["component"]
                    self.component[coid] =  \
                        { "urn:lri:property_type:id":make_ccss_id('standard_component',coid),
                          "urn:ccss:property_type:ccid":r['dot_id'],
                          "urn:lri:property_type:description":rec['text'],
                          "urn:lri:property_type:name":name_from_description(rec['text'],numwords=self.shortname_word_count),
                          "urn:lri:property_type:types": ["urn:lri:entity_type:thing",
                                                            "urn:lri:entity_type:competency", 
                                                            "urn:lri:entity_type:competency_container", 
                                                            "urn:lri:entity_type:learning_objective",
                                                            "urn:ccss:entity_type:standard_component"]}
                    self.standard[sid]["urn:lri:property_type:contains"].append(make_ccss_id('standard_component',coid))

    def dedupe(self):

        for i in self.initiative.values():
            i["urn:lri:property_type:contains"] = sorted(list(set(i["urn:lri:property_type:contains"])))
        for i in self.framework.values():
            i["urn:lri:property_type:contains"] = sorted(list(set(i["urn:lri:property_type:contains"])))
        for i in self.set.values():
            i["urn:lri:property_type:contains"] = sorted(list(set(i["urn:lri:property_type:contains"])))
        for i in self.grade.values():
            i["urn:lri:property_type:contains"] = sorted(list(set(i["urn:lri:property_type:contains"])))
        for i in self.domain.values():
            i["urn:lri:property_type:contains"] = sorted(list(set(i["urn:lri:property_type:contains"])))
        for i in self.standard.values():
            if "urn:lri:property_type:contains" in i:
                i["urn:lri:property_type:contains"] = sorted(list(set(i["urn:lri:property_type:contains"])))
        for i in self.anchor.values():
            i["urn:ccss:property_type:anchors"] = sorted(list(set(i["urn:ccss:property_type:anchors"])))
        for i in self.anchsect.values():
            i["urn:ccss:property_type:contained_anchor_standard"] = sorted(list(set(i["urn:ccss:property_type:contained_anchor_standard"])))
        for i in self.strand.values():
            i["urn:ccss:property_type:includes_domain"] = sorted(list(set(i["urn:ccss:property_type:includes_domain"])))
            i["urn:ccss:property_type:includes_anchor_standard"] = sorted(list(set(i["urn:ccss:property_type:includes_anchor_standard"])))
    def render(self):
        
        self.out = {}
        
        for k,v in self.initiative.items()+self.framework.items()+self.set.items()+self.grade.items()+self.domain.items()+self.standard.items()+self.component.items()+self.cluster.items()+self.anchor.items()+self.anchsect.items()+self.strand.items():
            self.out[v['urn:lri:property_type:id']] ={"action":"entity/create",
                                                        "q": v,
            "opts":{"access_token":"letmein"}}


    def write_suite(self,outformat='yaml'):

        if outformat == 'json':
            fh = open("./test_suites/load/ccss_suite_new.json",'w')
            fh.write(json.dumps(self.out,indent=4,sort_keys=True))
            fh.close()
        else:
            fh = open("./test_suites/load/ccss_suite_new.yaml",'w')
            fh.write(yaml.dump(self.out))
            fh.close()
            
                    
    
                
            


    def save_validation_report(self,outfile='./validation_report.json'):
        fh = open(outfile,'w')
        fh.write(json.dumps({'duplicates':self.dupes,
                             'missing_dot_id':self.missing_dot_id,
                             'invalid':self.bad_record},indent=4,sort_keys=True))
        fh.close()

if __name__ == '__main__':

    if len(sys.argv) > 1:
        lridir = sys.argv[1]
    else:
        lridir = "."
    
    cx = ccss_xml(mathfilename=lridir+"/external_schema/Math.xml",
                  elafilename=lridir+"/external_schema/ELA-Literacy.xml",
                  outfilename=lridir+"/test_suites/load")
    cx.parse()
    cx.save_validation_report()
    cx.process_math()
    cx.process_ela()
    cx.dedupe()
    cx.render()
    cx.write_suite()
    print json.dumps(cx.m,indent=4)
    print json.dumps(cx.e,indent=4)
    

    
