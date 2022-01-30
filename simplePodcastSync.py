#!/usr/bin/env python3
import os

import sys
import shutil
import json

with open('simplePodcastSync_Setup.json') as json_file:
    setupData = json.load(json_file)

"""# Directly from dictionary
with open('json_data.json', 'w') as outfile:
    json.dump(json_string, outfile)
  
# Using a JSON string
with open('json_data.json', 'w') as outfile:
    outfile.write(json_string)
"""

#dirSrc = "C:/Users/jayst/Documents/gPodder/Downloads"
#dirDest = "G:/Podcasts"
dirSrc = setupData['SourcePath']
dirDest = setupData['DestinationPath']
mode = setupData['Mode']

#print(dirSrc+", "+dirDest+", "+mode)

json_file.close()

### Check end of pathes are valid and correct   ####################
if dirSrc[len(dirSrc)-1] != "/":
    dirSrc = dirSrc+"/"
if dirDest[len(dirDest)-1] != "/":
    dirDest = dirDest+"/"

### Check if source path available  ################################
def checkPath(dirname):
    if (os.path.exists(dirname) == False):
        print("### paht not found: "+dirname)
        return False
    else:
        return True
"""
if len(sys.argv) > 3 :
    print("Parameter missmatch -> stop script")
    sys.exit(0)
elif len(sys.argv) == 1 :
    NotImplemented
elif len(sys.argv) == 2 :
    if (checkPath(sys.argv[1]) == False):
        sys.exit(0)
    else:
        dirSrc = sys.argv[1]
else :
    if (checkPath(sys.argv[1]) == False):
        sys.exit(0)
    else:
        dirSrc = sys.argv[1]
        dirDest = sys.argv[2]
"""

print("### Source: " + dirSrc)
print("### Destination: " + dirDest)

### Function to read out elements in a folder   ####################
def folder_objects(dirname, otype = "all"):
    if (os.path.exists(dirname) == False or
        os.path.isdir(dirname) == False or
        os.access(dirname, os.R_OK) == False):
        return False
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


### Read out elements in source folder  ############################
srcFolders = folder_objects(dirSrc)

### Check if elements available in source folder    ################
if len(srcFolders) == 0:
    print("### Source folder empty!")
    sys.exit(0)
'''else:
    print("### Podcasts to sync:")
    for folder in srcFolders:
        print(folder)
'''
####################################################################
### Sync with source    ############################################
####################################################################

#######################################################
### definitions / functions ###########################

### Copy compleate podcast folder   ###################
def copyAll(srcPath, destPath, srcFolders):
    print("### Copy whole podcasts to device")
    for srcFolder in srcFolders:
        print("### COPY: " + srcFolder)
        shutil.copytree(srcPath+srcFolder, destPath+srcFolder)

#######################################################
### Sync implementation ###############################

### 1. Destination does not exist -> copy all  ########
if (os.path.exists(dirDest) != True):
    os.mkdir(dirDest)
    copyAll(dirSrc, dirDest, srcFolders)
    sys.exit(0)

### Read out elements in destination folders    ########
destFolders = folder_objects(dirDest)

### 2. Destination is empty -> copy all ################
if len(destFolders) == 0:
    print("### No podcast on device -> Copy whole podcast to device")
    copyAll(dirSrc, dirDest, srcFolders)
    sys.exit(0)

### 3. Sync folder wize ################################
### 3.1 Check content for every source folder   ########
for srcFolder in srcFolders:
    ### Check if podcast folder is on device
    print("### Syncronsing: "+srcFolder)
    for destFolder in destFolders:
        ### if podcast directory exists on device
        if(destFolder == srcFolder):
            srcFolderContent = folder_objects(dirSrc+srcFolder)
            
            ### If no content in source folder -> delete destination folder
            if(srcFolderContent == 0):
                print("### No content - deleting directory on device")
                shutil.rmtree(dirDest+destFolder)
                break

            destFolderContent = folder_objects(dirDest+destFolder)
            ### Else, sync content to device    ########
            for srcContent in srcFolderContent:
                for destContent in destFolderContent:
                    if (destContent == srcContent):
                        print("    ### UP TO DATE: "+ srcContent)
                        break
                else: ### If source content is not on device
                    print("    ### COPY: "+srcContent)
                    shutil.copyfile(dirSrc+srcFolder+"/"+srcContent, dirDest+destFolder+"/"+srcContent)
            
            ### Delete device content which is not in sourec
            for destContent in destFolderContent:
                ### if the file is the *.POS (position) -> skip
                if(destContent[len(destContent)-1] != "S" ): 
                    ### ELSE -> check if device file is available at source directory
                    for srcContent in srcFolderContent:
                        if (srcContent == destContent):
                            break
                    else:
                        try:
                            print("    #### REMOVE: " + destContent)
                            os.remove(dirDest+destFolder+"/"+destContent)
                        except OSError as e:
                            print(f"    ### Error:{ e.strerror}")
            break 
    ### source content not on device -> copy source folder
    else:
        print("### New podcast -> COPY: " + srcFolder)
        print(dirSrc+srcFolder)
        print(dirDest+srcFolder)
        shutil.copytree(dirSrc+srcFolder, dirDest+srcFolder)

input("Press Enter to close ...")

sys.exit(0)


""" 

if (os.path.exists(dirDest) != True):
    os.mkdir(dirDest)

else:
    print("### Source folder already exists! -> End")
    sys.exit(0)

#    shutil.rmtree(dirDest)


### Check elements in source folder for episodes    ################
#for folder in srcFolder

### Delet destination folder    ####################################
print("\r\n### Clear destination path\r\n")
if (os.path.exists(dirDest) == True):
    shutil.rmtree(dirDest)

### Create empty destination folder ################################
os.mkdir(dirDest)
"""

"""
i = 0

for folder in srcFolders:
    for scrFolder in listCodeSrcFolders:
#        print(folder)
        if scrFolder in folder_objects(dirSrc+"/"+folder):
            shutil.copytree(dirSrc+folder+"/"+scrFolder, dirDest+"/"+scrFolder)
            i = i + 1
            print(dirSrc+folder+"/"+scrFolder)
"""
