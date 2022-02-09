#!/usr/bin/python
import os
import sys
import json


class SetupData():
    '''
    def __init__(self, SrcDir, DestDir, SyncMode, CoverSize):       
        self.srcDir = SrcDir
        self.destDir = DestDir
        self.synMmode = SyncMode
        self.coverSize = CoverSize
    '''
    SrcDir: str = ""
    DestDir:str = ""
    SyncMode:str = ""
    CoverSize:int = 0
    
    def init(self, SrcDir, DestDir, SyncMode, CoverSize):       
        self.SrcDir = SrcDir
        self.DestDir = DestDir
        self.SyncMode = SyncMode
        self.CoverSize = CoverSize
  
    def load(self, Filename):
        data = SetupData()
        data = readSetupData(Filename)
        self.SrcDir = data.SrcDir
        self.DestDir = data.DestDir
        self.SyncMode = data.SyncMode
        self.CoverSize = data.CoverSize
  
### Check if source path available  ################################
def checkPath(dirname):
    if (os.path.exists(dirname) == False):
#        print("### paht not found: "+dirname)
        return False
    else:
        return True


def readSetupData(FileName):
    if(checkPath(FileName) == False):
        print("### Setup file *"+FileName+"* not found!")
        input("\r\n### -> EXIT\r\nPress Enter to close ...")
        sys.exit(0)
    else:
        data = SetupData()
        with open(FileName) as json_file:
            jsonData = json.load(json_file)
            data.SrcDir = jsonData['SourcePath']
            data.DestDir = jsonData['DestinationPath']
            
            ### Check end of pathes are valid and correct   ####################
            if data.SrcDir[len(data.SrcDir)-1] != "/":
                data.SrcDir = data.SrcDir+"/"
            if data.DestDir[len(data.DestDir)-1] != "/":
                data.DestDir = data.DestDir+"/"

            data.SyncMode = jsonData['Mode']
            data.CoverSize = int(jsonData['AlbumCoverSize'])
        
        json_file.close()
        return data
    """
    # Directly from dictionary
    with open('json_data.json', 'w') as outfile:
        json.dump(json_string, outfile)
    
    # Using a JSON string
    with open('json_data.json', 'w') as outfile:
        outfile.write(json_string)
    """
