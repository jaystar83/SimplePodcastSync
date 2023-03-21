#!/usr/bin/python
import os
from .Setup import checkPath
from .fileOperations import readFolderObjects

class PlaylistGenerator():
    """    
    #EXTM3U
    #EXTINF:3634,HipHop Workout Remix 01
    F:\Music\Diverse\WorkOut Music\WorkOut Music\HipHop Workout Remix 01.mp3
    """
    m3uPL_Start: str = "#EXTM3U"
    m3uPL_Info: str = "#EXTINF:-1,"
    m3uPL_FilePrefix: str = "#"

    m3uPL_NewPCs: str = "#_NewPodcasts.m3u"
    newPlString: str =  m3uPL_Start

    def createPLsForPodcasts(self, DestDir, DestFolders, PLDestFolder):
        playlists = readFolderObjects(PLDestFolder)
        if(len(playlists) > 0):
            print("### DELETING OLD PLAYLISTS")
        for pl in playlists:
            if pl[0] == "#":
                print("    ### DELETING: " + PLDestFolder + pl)
                os.remove(PLDestFolder + pl)

        if(len(DestFolders) > 0):
            print("### CREATING NEW PLAYLISTS")

        for destFolder in DestFolders:
            plName :str = "#" + destFolder + ".m3u"
            plContent :str = self.m3uPL_Start
            episodeList = readFolderObjects(DestDir+destFolder)
            import eyed3 
            
            createPlFlag = False

            for episode in episodeList:
                if(episode[len(episode)-1] == "3"):
                    createPlFlag = True
                    tempAudiofile= eyed3.load(DestDir+destFolder+"/"+episode)
                    plContent = plContent + "\n" + self.m3uPL_Info + tempAudiofile.tag.title
                    plContent = plContent + "\n" + DestDir+destFolder+"/"+episode

            if(createPlFlag):
                print("    ### CREATING: " + plName)
                plContentCompleted = plContent.replace("/", "\\")
                f = open(PLDestFolder+plName , "w")
                f.write(plContentCompleted)
                f.close()

        print("    ### CREATING: " + self.m3uPL_NewPCs )
        plContentCompleted = self.newPlString.replace("/", "\\")
        f = open(PLDestFolder+self.m3uPL_NewPCs , "w")   
        f.write(plContentCompleted)
        f.close()


        #TBD

    def addToPLOfNewPodcats(self, EpisodePath, EpisodeTitle):
        self.newPlString = self.newPlString + "\n" + self.m3uPL_Info + EpisodeTitle
        self.newPlString = self.newPlString + "\n" + EpisodePath
        #TBD

