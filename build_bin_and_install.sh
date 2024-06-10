#!/bin/sh

# enter your username
USER="YourUserName"

pyinstaller --onefile --icon=Images/SIMPOSYum.ico SIMPOSYum.py

rm -r "/home/$USER/Programs/SIMPOSYum"
mkdir "/home/$USER/Programs"
mkdir "/home/$USER/Programs/SIMPOSYum"

cp "dist/SIMPOSYum" "/home/$USER/Programs/SIMPOSYum/SIMPOSYum"
#copy "dist\SIMPOSYum_SetupGui.exe" "SIMPOSYum_EXE\SIMPOSYum_SetupGui.exe"
cp "Images/SIMPOSYum.ico" "/home/$USER/Programs/SIMPOSYum/SIMPOSYum.ico"
cp "SIMPOSYum_Setup.json" "/home/$USER/Programs/SIMPOSYum/SIMPOSYum_Setup.json"
cp "SIMPOSYum_Setup.json" "/home/$USER/Programs/SIMPOSYum/SIMPOSYum_Setup_backup.json"

cp RUN_SIMPOSYum.sh RUN_SIMPOSYum.sh_tmp
sed -i "s|uSER|$USER|g" RUN_SIMPOSYum.sh_tmp
cp RUN_SIMPOSYum.sh_tmp "/home/$USER/Programs/SIMPOSYum/RUN_SIMPOSYum.sh"
rm RUN_SIMPOSYum.sh_tmp

cp SIMPOSYum.desktop SIMPOSYum.desktop_tmp
sed -i "s|uSER|$USER|g" SIMPOSYum.desktop_tmp
rm /home/$USER/.local/share/applications/SIMPOSYum.desktop
cp SIMPOSYum.desktop_tmp /home/$USER/.local/share/applications/SIMPOSYum.desktop
rm SIMPOSYum.desktop_tmp

# timeout 10