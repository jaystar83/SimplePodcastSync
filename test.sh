#!/bin/sh

# enter your username
USER="jaystar"

cp SIMPOSYum.desktop SIMPOSYum.desktop_tmp
sed -i "s|uSER|$USER|g" SIMPOSYum.desktop_tmp

cp SIMPOSYum.desktop_tmp /home/jaystar/.local/share/applications/SIMPOSYum.desktop

rm SIMPOSYum.desktop_tmp
# timeout 10