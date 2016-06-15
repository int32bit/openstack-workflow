#!/usr/bin/python
# coding=utf-8
# vim ts=4

import urllib
import re
import os.path

from os import walk

def getSequenceDiagram(wsdfile, outputFile, style = 'default'):
    request = {}
    assert os.path.isfile(wsdfile)
    with open(wsdfile, "r") as f:
        message = f.read()
    request["message"] = message
    request["style"] = style
    request["apiVersion"] = "1"

    url = urllib.urlencode(request)

    line = None
    try :
        f = urllib.urlopen("http://www.websequencediagrams.com/", url)
        line = f.readline()
        f.close()
    except IOError as e:
        print(e)
        return false
    expr = re.compile("(\?(img|pdf|png|svg)=[a-zA-Z0-9]+)")
    m = expr.search(line)

    if m == None:
        print "Invalid response from server."
        return False

    urllib.urlretrieve("http://www.websequencediagrams.com/" + m.group(0),
            outputFile)
    return True

def getSources(root="./src"):
    sources = []
    for (root, _, files) in walk("src"):
        for f in files:
            if f.endswith(".wsd"):
                sources.append(os.path.join(root, f))
    return sources

def generate(src="./src", target="./output", format="png", style="modern-blue"):
    for f in getSources(src):
        src_path = os.path.dirname(f)
        src_file = os.path.basename(f)
        target_path = target + src_path[src_path.index('/'):]
        output_file = src_file[:src_file.rindex('.') + 1] + format

        if not os.path.isdir(target_path):
            os.makedirs(target_path)
        output = target_path + "/" + output_file
        print("generating %s ..." % output)
        if getSequenceDiagram(f, output, style):
            print("Succeed to generate %s!" % output)
        else:
            print("Failed to generate %s!" % output)

def main():
    generate("src", "output", "png", "modern-blue") # png only, svg & pdf must register and pay 15$.

if __name__ == "__main__":
    main()
