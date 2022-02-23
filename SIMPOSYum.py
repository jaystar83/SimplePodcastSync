#!/usr/bin/env python3
import os
import sys

from Utils import Setup
from Utils import MP3Sync

if __name__ == "__main__":

    config = Setup.SetupData()
    config.load('SIMPOSYum_Setup.json', WinActive=False)

    print("### Source:      - " + config.SrcDir)
    print("### Destination: - " + config.DestDir)

    ### Check if source path available  ################################
    if(Setup.checkPath(config.SrcDir) == False):
        print("### Source not found: "+config.SrcDir)
        input("\r\n### -> EXIT\r\nPress Enter to close ...")
        sys.exit(0)
    ### Read out elements in source folder  ############################
    srcFolders = MP3Sync.readFolderObjects(config.SrcDir)

    ### Check if destination path available #############################
    if(Setup.checkPath(config.DestDir) == False):
        print("### Source not found: "+config.DestDir+" -> creating folder!")
        try:
            os.mkdir(config.DestDir)       
        except (IOError, KeyError) as e:
            print('    ###: Could not create folder!')
            print('    ###: ERROR: '+str(e))
            input("\r\n### -> EXIT\r\nPress Enter to close ...")
            sys.exit(0)

    ### Read out elements in source folder  ############################
    destFolders = MP3Sync.readFolderObjects(config.DestDir)
        
    ### Check if elements available in source folder    ################
    if len(srcFolders) == 0:
        print("### Source folder empty!")
        input("\r\n### -> EXIT\r\nPress Enter to close ...")
        sys.exit(0)
    '''else:
        print("### Podcasts to sync:")
        for folder in srcFolders:
            print(folder)
    '''
    ####################################################################
    ### Sync with source    ############################################
    ####################################################################
    MP3Sync.syncMP3content(config.SrcDir, srcFolders, config.DestDir, destFolders, config.CoverSize, config.SyncMode)

    input("\r\n### FINISHED\r\nPress Enter to close ...")
    sys.exit(0)

