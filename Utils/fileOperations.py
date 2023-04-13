#!/usr/bin/python
import os

####################################################################
### Function to read out elements in a folder   ####################
####################################################################
def readFolderObjects(dirname, otype = "all"):
    if (os.path.exists(dirname) == False or
        os.path.isdir(dirname) == False or
        os.access(dirname, os.R_OK) == False):
    return []
    else:
        objects = os.listdir(dirname)
        result = []
        for objectname in objects:
            objectpath = dirname + "/" + objectname
            if (otype == "all" or
                (otype == "dir"  and os.path.isdir(objectpath)  == True) or
                (otype == "file" and os.path.isfile(objectpath) == True) or
                (otype == "link" and os.path.islink(objectpath) == True)):
                result.append(objectname)
        result.sort()
        return result

