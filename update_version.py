# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime

def replace(root, replace_dict):
    if root[-1] == "/":
        root = root[0:-1]

    for x in os.listdir(root):
        path = root + "/" + x
    
        if os.path.isdir(path):
            replace(path, replace_dict)
      
        else:
            p, sep, ext = path.partition('.')
            if ext in ("py", "py.tmpl"):
                replaced = False
                infile = open(path, "r+")
                text = infile.read()
                infile.seek(0)
                for old_string, new_string in replace_dict.items():
                    if text.find(old_string) != -1:
                        text = text.replace(old_string, new_string)
                        replaced = True
                        infile.seek(0)
                infile.truncate()
                infile.write(text)
                if replaced:
                    print "Replaced in " + path
                infile.close()        

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s <new_version>" % sys.argv[0]
        sys.exit(1)
    
    ref_file = open("djangoerp/__init__.py")
    text = ref_file.read()
    ref_file.close()
    replace_dict = {}
    for line in text.split("\n"):
        if line.startswith("__copyright__"):
            replace_dict[line] = "__copyright__ = 'Copyright (c) 2013-%d, django ERP Team'" % datetime.now().year
        if line.startswith("__version__"):
            replace_dict[line] = "__version__ = '%s'" % sys.argv[1]
    replace("djangoerp", replace_dict)
