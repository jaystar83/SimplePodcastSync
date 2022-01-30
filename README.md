# SimplePodcastSync
Simple script / executable to synchronise podcasts with the mp3 player ( - Python 3 - )

## Instrucrtions:
### Creating the executable
* if not already done, install "pyinstaller"
  * ``` > pip3 install pyinstaller ```
* use pyinstaller to create *.exe
  * ``` > pyinstaller.exe --onefile --icon=Images\simplePodcastSync.ico .\simplePodcastSync.py ```
* copy executable from forlder "/dist" to folder "/SimplePodcastSync
* copy "simplePodcastSync_Setup.json" to folder "/SimplePodcastSync  

### Configuration
* using "simplePodcastSync_Setup.json"
    * "SourcePath": "C:/Users/<YourUserFoleer>/Documents/gPodder/Downloads",
        - Source directory
    * "DestinationPath": "G:/Podcasts",
        - Destination on your device
    * "Mode": "strict"
        - strict: overwriting and deleting during synchronisation -> Source is master
        - smooth: just copying new files