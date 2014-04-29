#!/usr/bin/python

import os.path
import subprocess
import sys

#./query_sequencer.py 192.168.100.75:9200 test_suites/paths/math/K/ccss_add_path_Math_K.json

hostname = sys.argv[1]
hostport = sys.argv[2]
pathsFile = sys.argv[3]

fh = open(pathsFile)
lines = fh.readlines()
pathFiles = []
for line in lines:
    line = line.strip()
    pathFiles.append(line)
fh.close()

cmd = os.path.abspath("../../query_sequencer.py")
output = ""
errors = ""
for pathFile in pathFiles:
    tmp = "processing: %s" % pathFile
    print(tmp)
    output += tmp
    errors += tmp

    args = [cmd, "%s:%s" % (hostname, hostport), pathFile]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    
    output += out
    errors += err

    tmp = "\n"
    output += tmp
    errors += tmp

name, ext = os.path.splitext(pathsFile)
outputFile = "./%s-output%s" % (name, ext)
fh = open(outputFile, "w")
fh.write(output)
fh.close()

errorsFile = "./%s-errors%s" % (name, ext)
fh = open(errorsFile, "w")
fh.write(errors)
fh.close()
print ("cat %s" % outputFile)
print ("cat %s" % errorsFile)

