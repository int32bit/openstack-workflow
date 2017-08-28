#!/usr/bin/python
# coding=utf-8
# vim ts=4

import urllib
import re
import os.path

from optparse import OptionParser
from os import walk


def getSequenceDiagram(wsdfile, outputFile, style='default'):
    request = {}
    assert os.path.isfile(wsdfile)
    with open(wsdfile, "r") as f:
        message = f.read()
    request["message"] = message
    request["style"] = style
    request["apiVersion"] = "1"

    url = urllib.urlencode(request)

    line = None
    try:
        f = urllib.urlopen("http://www.websequencediagrams.com/", url)
        line = f.readline()
        f.close()
    except IOError as e:
        print(e)
        return False
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


def generate(src="src", target="output", format="png", style="modern-blue",
             rebuild=False):
    for f in getSources(src):
        src_path = os.path.dirname(f)
        src_file = os.path.basename(f)
        target_path = target + src_path[src_path.index('/'):]

        work_path = os.getcwd() + "/"
        output_file_name = src_file[:src_file.rindex('.') + 1] + format
        target_full_path = work_path + target_path + "/" + output_file_name
        if os.path.exists(target_full_path) and not rebuild:
            print("Output file: %s already exists, skip it" % output_file_name)
            continue

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
    styles = [
        "default",
        "rose",
        "qsd",
        "napkin",
        "vs2010",
        "patent",
        "omegapple",
        "modern-blue",
        "earth",
        "roundgreen",
        "magazine"
    ]
    style_s = ", ".join(styles)

    parser = OptionParser()
    parser.add_option("-r", "--rebuild", dest="rebuild", default=False,
                      help="Rebuild exist output image")
    parser.add_option("-f", "--format", dest="out_format", default="png",
                      choices=["png", "svg", "pdf"],
                      help="Specify the output format, only png is free")
    parser.add_option("-s", "--style", dest="out_style", default="modern-blue",
                      choices=styles,
                      help="Specify the output style, "
                           "you can choose from: %s" % style_s)

    (options, args) = parser.parse_args()
    if not options.rebuild:
        print "The current generation will not overwrite old file!"
    generate("src", "output", options.out_format,
             options.out_style, rebuild=options.rebuild)

if __name__ == "__main__":
    main()
