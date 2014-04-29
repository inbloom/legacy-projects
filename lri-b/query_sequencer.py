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
import client,json,yaml,traceback,sys,re,hashlib,random,datetime

def resolve_xtract(x):
    return([s.strip() for s in x.split('|')])

def random_id():
    return 'urn:random:'+hashlib.md5(str(random.random())).hexdigest()[0:8]+"_"+datetime.datetime.utcnow().isoformat()


class query_sequencer(object):
    
    def __init__(self,host='localhost',port=8000, suitefilename=None):
        
        self.suitefilename = suitefilename
        self.outfilename = None
        self.host = host
        self.port = port
        self.var={}  # Holds resolved variables
        self.data={}
        self.step={}
        self.steporder=[]
        self.errors=[]
        self.result={}
        try:
            self.client = client.client(host=self.host,port=self.port)
        except:
            self.errors.append("FATAL! Could not open client connection! "+repr(self.host)+":"+repr(self.port))

        if self.client.errors:
            self.errors.extend(self.client.errors)

    def load(self):  
        
        # Strip comments
        goodlines = []
        fh = open(self.suitefilename)
        for line in fh:
            if line.strip().startswith("//"):
		continue
            goodlines.append(line)

        # Parse the suite
        try:
            if self.suitefilename.endswith('.yaml'):
                self.data = yaml.load(''.join(goodlines))
                self.stem = self.suitefilename.replace('.yaml','')
                self.suffix=".yaml"
            elif self.suitefilename.endswith('.json'):
                self.data = json.loads(''.join(goodlines))
                self.stem = self.suitefilename.replace('.json','')
                self.suffix=".json"
            else:
                self.errors.append("Unknown input file format.  Make sure your extension is one of '.yaml' or '.json'.")
                return False
        except Exception, e:
            self.errors.append("Failed to load test suite file %s with error = %s" %(self.suitefilename,traceback.format_exc()))
            return False

        # We always sort by 
        for step_id in self.data:
            self.steporder.append(step_id)
        self.steporder.sort()

        return True

    def save_result(self):
        self.outfilename = self.stem+".report.json"
        ofh = open(self.outfilename,'w')
        ofh.write(json.dumps(self.final_result,indent=4,sort_keys=True))
        ofh.close()

    def parse_step(self,step_id):

        t = {}

        if step_id not in self.data:
            self.errors.append("Step '%s': not in test suite data." % (step_id))
            return False

        if 'q' not in self.data[step_id]:
            self.errors.append("Missing 'q' from test '%s'." % (step_id))
            return False

        try:
            t['q'] = self.data[step_id]['q']
        except Exception, e:
            self.errors.append("Step '%s' field 'q' has unparseable JSON." % (step_id)) 
            #print traceback.format_exc(),type(self.data[step_id])
            return False

        if 'action' not in self.data[step_id]:
            self.errors.append("Missing 'action' from step '%s'." % (step_id))
            return False

        t['action'] = self.data[step_id]['action'] 

        if 'opts' not in self.data[step_id] and self.data[step_id]['action'] == 'entity/search':
            self.errors.append("Missing 'opts' from entity/search step '%s'." % (step_id))
            return False

        try:
            t['opts'] = self.data[step_id].get('opts','{}')
        except Exception, e:
            self.errors.append("Step '%s' field 'opts' has unparseable JSON." % (step_id)) 
            #print traceback.format_exc(),self.data[step_id].get('opts','{}')
            return False


        # Resolve known variables in xtracts and tests and parse xtract

        xtracts = self.data[step_id].get('xtract',[])
        tests = self.data[step_id].get('test',[])

        xresolved = []
        for x in xtracts:
            xresolved.append([s.strip() for s in x.split('|')])

        t['xtract'] = xtracts
        #t['xtract'] = xresolved
        t['test'] = tests
            
        self.step[step_id] = t
        return True

    def run_single_step(self,step_id):

        result = { "status":"not_started",
                   "errors":[],
                   "component": [] }

        self.parse_step(step_id)

        if self.errors:
            result['status'] ='parse_fail'
            self.result[step_id] = result
            return False


        t = self.step[step_id]

        # Sub in vars to query
        q = json.dumps(t['q'])

        # We need random IDs in order to run tests multiple times
	while '$RANDOM_ID' in q:
	    q = q.replace('$RANDOM_ID',random_id(),1)

        # So subs for extracted variables
        for v in self.var:
            q = q.replace(v,self.var[v])
        t['q'] = json.loads(q)

        r = self.client.query(t['action'],t['q'],t['opts']) 
        result["server_response"] = r

        for i in range(len(t['xtract'])):
            x = resolve_xtract(t['xtract'][i])
            d = r
            for stp in range(0,len(x)-1):
                # Sub in case parts of the path are previous vars
                if x[stp] in self.var:
                    x[stp] = x[stp].replace(x[stp],self.var[x[stp]])

                # Make one step down the path
                if isinstance(d,dict):
                    d = d.get(x[stp])
                elif isinstance(d,list):
                    try:
                        #print stp,x[stp]
                        d = d[int(x[stp])]
                    except Exception, e:
                        result['status'] = 'failed'
                        result['errors'].append("Step %s:Not able to extract %s from result. (list element problem) " % (step_id,(' | '.join(x))))
                        print traceback.format_exc()
                        break   
                    
                if d == None:
                    result['status'] = 'failed'
                    result['errors'].append("Step %s:Not able to extract %s from result (dict element problem)" % (step_id,(' | '.join(x))))
                    break
            
            # Save our newly extracted variable
            if re.search("(\$[A-Z_]+)",x[-1]):        
                self.var[x[-1]] = d
                
        if result['errors']:
            result['status'] = 'failed'
            self.result[step_id] = result
            return False

        # Do our test components
        for i in range(len(t['test'])):
            compresult = {}

            comp = t['test'][i]
            compresult['raw']=comp

            # Sub vars
            for v in re.findall("(\$[A-Z_0-9]+)",comp):
		if v in self.var:
                    # print v,self.var
		    comp = comp.replace(v,str(self.var[v]))

            # do some escaping for the eval
            comp = comp.replace('\\','\\\\')
            comp = comp.replace('\\"','\\\"')

            compresult['resolved']=comp

            # Attempt test
            try:
                result['passed'] = eval(comp)
            except Exception, e:
                result['status'] = 'failed'
                result['errors'].append("Step %s: Test component '%s' (resolved to '%s') failed with python eval error." % (step_id,t['test'][i],comp))
                compresult["traceback"] = traceback.format_exc()
            
            result['component'].append(compresult)

        self.result[step_id] = result

	# If we had an error and did not pass our tests, then we failed
	if result['errors'] and result.get("passed") != True:
            result['status'] = 'failed'
            return False

        result['status'] = 'success'
        return True

    
    def run(self):

        self.final_result = { 'status':'not_started',
                              'vars':self.var,
                              'steps' : self.step,
                              'step_order': self.steporder,
                              'errors': self.errors }

        if self.errors:
            self.final_result['status'] ='startup (load or parse or connect) failure'
            return self.final_result


        self.final_result['status'] = 'running'

        for step_id in self.steporder:
            print "Running Step:",step_id
            self.run_single_step(step_id)
            self.step[step_id]['result'] = self.result[step_id]
            if self.result[step_id]['status'] != 'success' or self.result[step_id].get('passed') == False:
                self.final_result['status'] = 'incomplete'
                break  # We can't continue if we hit a processing failure or a failed test
            
        if self.final_result['status'] == 'running':
            self.final_result['status'] = 'complete'

        return self.final_result

   

if __name__=='__main__':

    host,port = sys.argv[1].split(':') 
    suitefilename = sys.argv[2]

    qt = query_sequencer(host=host,port=port,suitefilename=suitefilename)
    if qt.load():
        qt.run()
        qt.save_result()
        print "Done..."
    else:
        print "Unable to load suite because:",qt.errors




        
