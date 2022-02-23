#!/usr/bin/python3
import os
import sys
import json
import shutil
from tkinter import messagebox

errorCode = "E_OK"  ### No error

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
  
    def load(self, Filename, WinActive):
        data = SetupData()
        data = readSetupData(Filename, WinActive)
        if(errorCode == "E_OK"):
            self.SrcDir = data.SrcDir
            self.DestDir = data.DestDir
            self.SyncMode = data.SyncMode
            self.CoverSize = data.CoverSize

        return errorCode

    def save(self, Filename, WinActive):
        writeSetupData(self, Filename, WinActive)
        return errorCode
        
        
  
### Check if source path available  ################################
def checkPath(dirname):
    if (os.path.exists(dirname) == False):
#        print("### paht not found: "+dirname)
        return False
    else:
        return True


def readSetupData(FileName, WinActive):
    errorCode = "E_OK"
    if(checkPath(FileName) == False):
        if(WinActive):
            errorCode = "E_FileNotFound"
        else:
            print("### Setup file *"+FileName+"* not found!")
            input("\r\n### -> EXIT\r\nPress Enter to close ...")
            sys.exit(0)
    else:
        data = SetupData()
        with open(FileName) as json_file:
            jsonData = json.load(json_file)
            data.SrcDir = jsonData['SourcePath']
            data.DestDir = jsonData['DestinationPath']
            
            ### Check if filename are available ################################
            if(data.SrcDir == "" or data.SrcDir == 0):
                if(WinActive):
                    errorCode = "E_SrcPathInvalid"
                else:
                    print("### Source path invalid!")
                    input("\r\n### -> EXIT\r\nPress Enter to close ...")
                    sys.exit(0)

            if(data.DestDir == "" or data.DestDir == 0):
                if(WinActive):
                    errorCode = "E_DestPathInvalid"
                else:
                    print("### Destination path invalid!")
                    input("\r\n### -> EXIT\r\nPress Enter to close ...")
                    sys.exit(0)

            ### Check end of pathes are valid and correct   ####################
            if data.SrcDir[len(data.SrcDir)-1] != "/":
                data.SrcDir = data.SrcDir+"/"
            if data.DestDir[len(data.DestDir)-1] != "/":
                data.DestDir = data.DestDir+"/"

            data.SyncMode = jsonData['Mode']
            data.CoverSize = int(jsonData['AlbumCoverSize'])
        
        json_file.close()
        return data

def writeSetupData(Data, FileName, WinActive):
    errorCode = "E_OK"
    if(checkPath(FileName) == False):
        if(WinActive):
            errorCode = "E_FileNotFound"
        else:
            print("### Setup file *"+FileName+"* not found!")
            input("\r\n### -> EXIT\r\nPress Enter to close ...")
            sys.exit(0)
    else:
 #       jsonData
        with open(FileName) as json_file:
            jsonData = json.load(json_file)
        
        json_file.close()

        jsonData['SourcePath'] = Data.SrcDir 
        jsonData['DestinationPath'] = Data.DestDir 
            
        ### Check end of pathes are valid and correct   ####################
        jsonData['Mode'] = Data.SyncMode
        jsonData['AlbumCoverSize'] = Data.CoverSize

        jsonData['__comment'] = "configuerd with Setup Gui"

        with open(FileName, 'w') as outfile:
            json.dump(jsonData, outfile)
            print("output written ...")

        outfile.close()
        print("file closed")

    """
    # Directly from dictionary
    with open('json_data.json', 'w') as outfile:
        json.dump(json_string, outfile)
    
    # Using a JSON string
    with open('json_data.json', 'w') as outfile:
        outfile.write(json_string)
    """
def copyFile_save(SrcFile, DestFile):
    try:
        shutil.copyfile(SrcFile, DestFile)
        return 'E_OK'
    except shutil.Error as e:
        err = 'Error: %s' % e
        print(err)
        return err
    except IOError as e:
        err = 'Error: %s' % e.strerror
        print(err)
        return err
