@echo off


CALL "pyinstaller.exe" --onefile --icon=Images\SIMPOSYum.ico .\SIMPOSYum.py
CALL "pyinstaller.exe" --windowed --onefile --icon=Images\SIMPOSYum_SetupGui.ico .\SIMPOSYum_SetupGui.py

rmdir /s /q "SIMPOSYum_EXE"
mkdir "SIMPOSYum_EXE"

copy "dist\SIMPOSYum.exe" "SIMPOSYum_EXE\SIMPOSYum.exe"
copy "dist\SIMPOSYum_SetupGui.exe" "SIMPOSYum_EXE\SIMPOSYum_SetupGui.exe"
copy "Images\SPS_Config_Small.ico" "SIMPOSYum_EXE\SPS_Config_Small.ico"
copy "SIMPOSYum_Setup.json" "SIMPOSYum_EXE\SIMPOSYum_Setup.json"
copy "SIMPOSYum_Setup.json" "SIMPOSYum_EXE\SIMPOSYum_Setup_backup.json"

timeout 10