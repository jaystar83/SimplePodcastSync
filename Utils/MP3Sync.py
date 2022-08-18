#!/usr/bin/python
import os
from .Setup import checkPath

####################################################################
### Function to read out elements in a folder   ####################
####################################################################
def readFolderObjects(dirname, otype = "all"):
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

####################################################################
### Function to prepare Episode cover   ############################
####################################################################
from PIL import Image

def resizeAlbumFolder(InFile, OutFile, NewSize):
    im = Image.open(InFile)
    im = im.resize((NewSize, NewSize))
    #im = img_as_ubyte(im)
    im.save(OutFile)

def resizeAlbumCover_pngInput(InFile, OutFile, NewSize):
    im = Image.open(InFile)
    im = im.convert('RGB')
    im = im.resize((NewSize, NewSize))
    #im = img_as_ubyte(im)
    im.save(OutFile)

####################################################################
### Function to adapt and copy new content  ########################
####################################################################
import shutil
import eyed3 
from eyed3.id3.frames import ImageFrame # to change mp3 file album pic
#https://eyed3.readthedocs.io/en/latest/
#Python >= 3.6 is required.

#-------------------------------------------------------------------------------
### Synchronising the MP3 content in source with the device ####################
def syncMP3content(SrcDir, SrcFolders, DestDir, DestFolders, PicSize, SyncMode):
    for srcFolder in SrcFolders:
        print("### SYNC: "+srcFolder)
        srcFolderContent = readFolderObjects(SrcDir+srcFolder)

        ### 1. Check whether source folder contains epidsodes
        if(srcFolderContent == 0 or ( True == ( (len(srcFolderContent)==1) and srcFolderContent[0][len(srcFolderContent[0])-1] == "g") ) ):
            ### 1.1 No Epsiodes in source folder
            print("    ### EMPTY source folder")
            if(SyncMode == "strict"):
                if(checkPath(DestDir+srcFolder)==True):
                    deletFolder(DestDir, srcFolder)
            else:
                print("    ### NOTHING to synchronise")

        ### 2. Episodes available -> Synching
        else:
            ### 2.1 If Source does NOT exist on device -> create 
            if(checkPath(DestDir+srcFolder)==False):
                print("    ### CREATING episodes folder on decice")
                os.mkdir(DestDir+srcFolder)
                DestFolders.append(srcFolder)

            copyNewEpisodes(SrcDir, srcFolder, DestDir, DestFolders, PicSize, SyncMode)

#-------------------------------------------------------------------------------
### Check source and device and copy episode if not on device   ################
def copyNewEpisodes(SrcDir, SrcFolder, DestDir, DestFolders, PicSize, SyncMode):
    for destFolder in DestFolders:
        ### if podcast directory exists on device or 
        if(destFolder == SrcFolder):
            srcFolderContent = readFolderObjects(SrcDir+SrcFolder)
            destFolderContent = readFolderObjects(DestDir+destFolder)
            ### 2. Else, sync content to device    ########
            tempFolderPic = ""

            if(checkPath(SrcDir+SrcFolder+"/folder.jpg")):
                tempFolderPic = SrcDir+SrcFolder+"/folder_temp.jpg"
                resizeAlbumFolder(SrcDir+SrcFolder+"/folder.jpg", tempFolderPic, PicSize)

            if(checkPath(SrcDir+SrcFolder+"/folder.png")):
                tempFolderPic = SrcDir+SrcFolder+"/folder_temp.jpg"
                resizeAlbumCover_pngInput(SrcDir+SrcFolder+"/folder.png", tempFolderPic, PicSize)

            noUpdateForThisPodcast = True

            for srcContent in srcFolderContent:
                ### 2.1 Check is dest content is up tp date
                for destContent in destFolderContent:
                    if (destContent == srcContent):
#                        print("    ### UP TO DATE: "+ srcContent)
                        break

                ### 2.2 If source content is not on device
                else: 
                    if(srcContent[len(srcContent)-1] == "3"):   # is mp3 file?
                        noUpdateForThisPodcast = False
                        print("    ### COPY: "+srcContent)
                        ### Create temp file
                        shutil.copyfile(SrcDir+SrcFolder+"/"+srcContent, SrcDir+SrcFolder+"/"+"temp.sps")
                        tempAudiofile= eyed3.load(SrcDir+SrcFolder+"/"+"temp.sps")

                        try:
                            if(tempAudiofile.tag == None):
                                tempAudiofile.initTag()

                                #change mp3 file album cover if "folder.jpg/png" is available
                                #tempAudiofile.tag.images.set(ImageFrame.FRONT_COVER, open('cover.jpg','rb').read(), 'image/jpeg')

                                #change file info
                                tempAudiofile.tag.artist = SrcFolder
                                print("        ### Update artist: "+str(tempAudiofile.tag.artist))
                                tempAudiofile.tag.album = SrcFolder
                                print("        ### Update album: "+str(tempAudiofile.tag.album))
                                tempAudiofile.tag.title = srcContent[:len(srcContent)-4]
                                print("        ### Update title: "+str(tempAudiofile.tag.title))
                                tempAudiofile.tag.images.set(ImageFrame.FRONT_COVER, open(tempFolderPic,'rb').read(), 'image/jpeg')
                                tempAudiofile.tag.save()

                            else:
                                #change file info
                                trackArtis = ""
                                trackAlbum = ""
                                trackTitle = ""
                                trackNo = None
                                trackGenre = ""
                                if(tempAudiofile.tag.artist == None or tempAudiofile.tag.artist == "" or tempAudiofile.tag.artist == ";"):
                                    trackArtis = SrcFolder
                                    print("        ### Update artist: "+trackArtis)
                                else:
                                    trackArtis = tempAudiofile.tag.artist

                                if(tempAudiofile.tag.album == None or tempAudiofile.tag.album == "" or tempAudiofile.tag.album == ";"):
                                    trackAlbum = SrcFolder
                                    print("        ### Update album: "+trackAlbum)
                                else:
                                    trackAlbum = tempAudiofile.tag.album

                                if(tempAudiofile.tag.title == None or tempAudiofile.tag.title == "" or tempAudiofile.tag.title == ";"):
                                    trackTitle = srcContent[:len(srcContent)-4]
                                    print("        ### Update title: "+trackTitle)
                                else:
                                    trackTitle = tempAudiofile.tag.title

                                if(tempAudiofile.tag.track_num[0] == None or tempAudiofile.tag.track_num[0] == "" or tempAudiofile.tag.track_num[0] == ";"):
                                    print("        ### No tack number in: "+trackTitle)
                                else:
                                    trackNo = int(tempAudiofile.tag.track_num[0])

                                if(tempAudiofile.tag.genre == None or tempAudiofile.tag.genre == "" or tempAudiofile.tag.genre == ";"):
                                    trackGenre = "Podcast"
                                    print("        ### Update genre: "+trackGenre)
                                else:
                                    trackGenre = tempAudiofile.tag.genre

                                tempAudiofile.initTag()
                                tempAudiofile.tag.artist = trackArtis
                                tempAudiofile.tag.album = trackAlbum
                                tempAudiofile.tag.title = trackTitle
                                tempAudiofile.tag.track_num = trackNo
                                tempAudiofile.tag.genre = trackGenre
                                tempAudiofile.tag.images.set(ImageFrame.FRONT_COVER, open(tempFolderPic,'rb').read(), 'image/jpeg')
                                tempAudiofile.tag.save()

                        except:
                            print("        ### mp3 tag invalid, just copying: "+srcContent)
 
                        shutil.copyfile(SrcDir+SrcFolder+"/"+"temp.sps", DestDir+destFolder+"/"+srcContent)
                        os.remove(SrcDir+SrcFolder+"/"+"temp.sps")

            if(noUpdateForThisPodcast):  
                print("    ### NO NEW EPISODES")
     
            if(tempFolderPic != ""):
                os.remove(tempFolderPic)

            if(SyncMode == "strict"):
                cleanupFolder(SrcDir, SrcFolder, DestDir, destFolder)

#-------------------------------------------------------------------------------
### Check device content and delete epsiodes that are not in source folder  ####
def cleanupFolder(SrcDir, SrcFolder, DestDir, DestFolder):
    destFolderContent = readFolderObjects(DestDir+DestFolder)        
    srcFolderContent = readFolderObjects(SrcDir+SrcFolder)
    for destContent in destFolderContent:
        if( destContent.endswith(".mp3") or destContent.endswith(".MP3") ):
            for srcContent in srcFolderContent:
                if(destContent == srcContent):
                    break
            else:
                
                print("    #### DELETING: " + destContent)
                destFile = DestDir+DestFolder+"/"+destContent
                filename, extension = os.path.splitext(destFile)
                
                if( checkPath(filename+".POS") ):
                    os.remove(filename+".POS")

                if( checkPath(filename+".pos") ):
                    os.remove(filename+".pos")
                    
                os.remove(destFile)

#-------------------------------------------------------------------------------
### Check device content and delete folders/epsiodes that are not in source ####
def cleanupDevice(SrcDir, SrcFolders, DestDir, DestFolders):
    print("\r\n### Cleaning up device:") 
    for destFolder in DestFolders:
        print('    ### CLEANUP: '+destFolder)
        ### 1. If source folder not exists -> delete destination folder
        if(checkPath(SrcDir+destFolder)==False):
            print("        ### DELETING: Source content not available -> deleting directory on device")
            shutil.rmtree(DestDir+destFolder)
        else:
            destFolderContent = readFolderObjects(DestDir+destFolder)        
            srcFolderContent = readFolderObjects(SrcDir+destFolder)
            ### 2. If no content in source folder -> delete destination folder                             "g" -> jpg / png
            if(srcFolderContent == 0 or ( (len(srcFolderContent)==1) and srcFolderContent[0][len(srcFolderContent[0])-1] == "g") ):
                print("        ### DELETING: No source content available -> deleting directory on device")
                shutil.rmtree(DestDir+destFolder)

            ### 3. Check content: If destination episodes not in source -> delete
            else:
                for destContent in destFolderContent:
                    for srcContent in srcFolderContent:
                        if(destContent == srcContent):
                            break
                    else:
                        print("        ### DELETING: " + destContent)
                        os.remove(DestDir+destFolder+"/"+destContent)

#-------------------------------------------------------------------------------
### Delet the given folder and wirte inb output ################################
def deletFolder(Dir, Folder):
    print("    ### DELETING: " + Folder)
    shutil.rmtree(Dir+Folder)


'''
#    destFolderContent = readFolderObjects(DestDir+destFolder)


    for destContent in destFolderContent:
        ### if the file is the *.POS (position) -> skip
        if(destContent[len(destContent)-1] != "S" ): 
            ### ELSE -> check if device file is available at source directory
            for srcContent in srcFolderContent:
                if (srcContent == destContent):
                    break
            else:
                try:
                    fileName = dirDest+destFolder+"/"+destContent
                    posiFileName_1 = fileName[:len(fileName)-3] + "POS"                          
                    posiFileName_2 = fileName[:len(fileName)-3] + "pos"                          

                    print("    #### REMOVE: " + destContent)
                    os.remove(fileName)

                    # also remove postion files (*.POS)  
                    if(os.path.isfile(posiFileName_1)):
                        print("    #### REMOVE: " + destContent[:len(destContent)-3]+"POS")
                        os.remove(posiFileName_1)
                    if(os.path.isfile(posiFileName_2)):
                        print("    #### REMOVE: " + destContent[:len(destContent)-3]+"pos")
                        os.remove(posiFileName_2)

                except OSError as e:
                    print(f"    ### Error:{ e.strerror}")
    break 
'''