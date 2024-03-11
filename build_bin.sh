#!/bin/sh

pyinstaller --onefile --icon=Images/SIMPOSYum.ico SIMPOSYum.py

rm -r "SIMPOSYum_BIN"
mkdir "SIMPOSYum_BIN"

cp "dist/SIMPOSYum" "SIMPOSYum_BIN/SIMPOSYum"
#copy "dist\SIMPOSYum_SetupGui.exe" "SIMPOSYum_EXE\SIMPOSYum_SetupGui.exe"
cp "Images/SPS_Config_Small.ico" "SIMPOSYum_BIM/SPS_Config_Small.ico"
cp "SIMPOSYum_Setup.json" "SIMPOSYum_BIN/SIMPOSYum_Setup.json"
cp "SIMPOSYum_Setup.json" "SIMPOSYum_BIN/SIMPOSYum_Setup_backup.json"

# timeout 10