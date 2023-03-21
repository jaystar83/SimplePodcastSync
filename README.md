# SimplePodcastSync
Simple script / executable to synchronise podcasts with the mp3 player ( - Python 3 - )

## Instrucrtions:
### Creating the executable
* if not already done, install "pyinstaller"
  * ``` > pip3 install pyinstaller ```
* use pyinstaller to create *.exe
  * run batch file to create *.exe files and add files to App folder
  * ``` > build_exe.bat ```
* This will create folder "SIMPOSYum_EXE" including all necessary files  

### Configuration
* using SIMPOSYum_SetupGui.exe - proposed
* OR using *SIMPOSYum_Setup.json*
    * "SourcePath": "C:/Users/*YourUserFolder*/Documents/gPodder/Downloads",
        - Source directory
    * "DestinationPath": "G:/Podcasts",
        - Destination on your device
    * "Mode": "strict"
        - strict: overwriting and deleting during synchronisation -> Source is master
        - smooth: just copying new files

### Using the executbale
* Copy the folder *SIMPOSYum_EXE* to you local folder
* Configure the *SIMPOSYum_Setup.json* (see above)
* for easy usage: Right Click - Send to - Desktop (Create shortcuts of *.exe files)

### Addotional Pythondependencies
* pip
  * python --version
  * py -m ensurepip --upgrade
  * python -m pip --version
* PIL
  * python3 -m pip install --upgrade pip
  * python3 -m pip install --upgrade Pillow
* eyed3
  * python3 -m pip install --upgrade eyeD3 python-magic-bin