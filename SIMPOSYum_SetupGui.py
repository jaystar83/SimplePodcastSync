#!/usr/bin/env python3
import sys
import os

import tkinter as tk
from tkinter import E, LEFT, RIGHT, ttk
from tkinter import filedialog
from tkinter import messagebox

from Utils import Setup
from Utils.GuiSupport import winHide
from Utils.Setup import copyFile_save


if (__name__ == "__main__"):    

    configFileName = 'SIMPOSYum_Setup.json'
    tempConfigFileName = 'temp_SIMPOSYum_Setup.json'

    def getSrcFolderPath():
        selectedSrcPath = str(filedialog.askdirectory())
        if(selectedSrcPath == "" or selectedSrcPath == 0):
            return -1
        else:
            configTemp = Setup.SetupData()
            errorCode = configTemp.load(tempConfigFileName, WinActive=True)
            check_LoadConfigError(errorCode, WinActive=True)
            if(errorCode == "E_OK"):
                configTemp.SrcDir = selectedSrcPath
                errorCode = configTemp.save(tempConfigFileName, WinActive=True)
                check_SaveConfigError(errorCode,WinActive=True)
                if(errorCode == "E_OK"):
                    tempSrcFolderLabel.config(text = " -> " + selectedSrcPath)
                    return 0               
        return -1

    def getDestFolderPath():
        selectedDestPath = str(filedialog.askdirectory())
        if(selectedDestPath == "" or selectedDestPath == 0):
            return -1
        else:
            configTemp = Setup.SetupData()
            errorCode = configTemp.load(tempConfigFileName, WinActive=True)
            check_LoadConfigError(errorCode, WinActive=True)
            if(errorCode == "E_OK"):
                configTemp.DestDir = selectedDestPath
                errorCode = configTemp.save(tempConfigFileName, WinActive=True)
                check_SaveConfigError(errorCode,WinActive=True)
                if(errorCode == "E_OK"):
                    tempDestFolderLabel.config(text = " -> " + selectedDestPath)
                    return 0                
        return -1

    def syncModeUpdate():
        configTemp = Setup.SetupData()
        errorCode = configTemp.load(tempConfigFileName, WinActive=True)
        check_LoadConfigError(errorCode, WinActive=True)
        if(errorCode == "E_OK"):
            configTemp.SyncMode = tempSyncMode.get()
            errorCode = configTemp.save(tempConfigFileName, WinActive=True)
            check_SaveConfigError(errorCode,WinActive=True)
            if(errorCode == "E_OK"):
                tempSyncModeLabel.config(text=" -> Selected SyncMode: "+tempSyncMode.get())
        
    def saveConfigData(SrcFile, DestFile):
        ret = copyFile_save(SrcFile, DestFile)
        if(ret == 'E_OK'):
            messagebox.showinfo("Save config file","Config saved successfully")
            configTemp = Setup.SetupData()
            errorCode = configTemp.load(tempConfigFileName, WinActive=True)
            check_LoadConfigError(errorCode, WinActive=True)
            if(errorCode == "E_OK"):
                confSrcFolderLabel.config(text= 'Configured source -> ' + configTemp.SrcDir)
                confDestFolderLabel.config(text= 'Configured source -> ' + configTemp.DestDir)
                confSyncModeLabel.config(text='Configured synchronisation mode -> ' + configTemp.SyncMode)
        else:
            messagebox.showerror("Save config file error", ret)

    def check_LoadConfigError(errorCode, WinActive):
        if(errorCode != "E_OK"):
            if(errorCode == "E_FileNotFound"):
                messagebox.showerror("Load config file error", "File not found!")
            elif(errorCode == "E_SrcPathInvalid"):
                messagebox.showerror("Load config file error", "Source path invalid!")
            elif(errorCode == "E_DestPathInvalid"):
                messagebox.showerror("Load config file error", "Destination path invalid!")
            else:
                messagebox.showerror("Load config file error", "Could not load Setup Data!")

            if(WinActive == False):
                sys.exit(0)
                #win.quit()

    def check_SaveConfigError(errorCode, WinActive):
        if(errorCode != "E_OK"):
            if(errorCode == "E_FileNotFound"):
                messagebox.showerror("Save config - file error", "File not found!")
            else:
                messagebox.showerror("Load config - file error", "Could not save Setup Data!")

            if(WinActive == False):
                sys.exit(0)

#    winHide("SIMPOSYum_SetupGui.exe")

    config = Setup.SetupData()
    errorCode = config.load( configFileName, WinActive=False)
    check_LoadConfigError(errorCode, False)

    errorCode = copyFile_save(configFileName, tempConfigFileName)
    if(errorCode != 'E_OK'):
        messagebox.showerror("File save error", errorCode)
        sys.exit(0)

    win = tk.Tk()
    win.title('SIMPOSYum Config GUI')
    win.iconbitmap('SPS_Config_Small.ico')
    win.geometry("400x400")

    selectedSrcPath = config.SrcDir
    selectedDestPath = config.DestDir
    selectedSyncMode = config.SyncMode
    selectCoverSize =config.CoverSize
    
################################################################
### Menu bar    ################################################
################################################################
    menu = tk.Menu(win)
    win.config(menu=menu)
    subMenu_exit = tk.Menu(menu)
    menu.add_cascade(label="Exit_menu", menu=subMenu_exit)
    subMenu_exit.add_command(label="Exit", command=win.quit)

################################################################
### Frame 1 - Source folader    ################################
################################################################
    frame1 = tk.Frame(win, bd=2)
    frame1.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.05)
    confSrcFolderLabel = tk.Label(frame1, text= 'Configured source -> ' + config.SrcDir)
    confSrcFolderLabel.pack(side=LEFT)

    frame11 = tk.Frame(win, bd=2)
    frame11.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.15)

    tempSrcFolderPath = tk.StringVar(frame11, config.SrcDir)

    btnFindSrc = tk.Button(frame11, text="Browse Folder",command=getSrcFolderPath)
    tempSrcFolderLabel = tk.Label(frame11, text=' -> '+tempSrcFolderPath.get())
    btnFindSrc.grid(row=1, column=0)
    tempSrcFolderLabel.grid(row=1,column=1)

################################################################
### Frame 2 - Destination folder    ############################
################################################################

    frame2 = tk.Frame(win, bd=2)
    frame2.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.05)
    confSrcFolderLabel.config(text= 'Configured source -> ' + config.SrcDir)

    confDestFolderLabel = tk.Label(frame2, text= 'Configured destination -> ' + config.DestDir)
    confDestFolderLabel.pack(side=LEFT)

    frame22 = tk.Frame(win, bd=2)
    frame22.place(relx=0.05, rely=0.30, relwidth=0.9, relheight=0.15)
    
    tempDestFolderPath = tk.StringVar(frame22, config.DestDir)

    btnFindDest = tk.Button(frame22, text="Browse Folder",command=getDestFolderPath)
    tempDestFolderLabel = tk.Label(frame22, text=' -> '+config.DestDir)
    btnFindDest.grid(row=1, column=0)
    tempDestFolderLabel.grid(row=1,column=1)

################################################################
### Frame 3 - Select SyncMode   ################################
################################################################
    frame3 = tk.Frame(win)
    frame3.place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.05 )
    confSyncModeLabel = tk.Label(frame3, text= 'Configured synchronisation mode -> ' + config.SyncMode)
    confSyncModeLabel.pack(side=LEFT)

    frame33 = tk.Frame(win)
    frame33.place(relx=0.05, rely=0.55, relwidth=0.9, relheight=0.15)

    tempSyncMode = tk.StringVar(frame33, config.SyncMode)
    tempSyncModeLabel = tk.Label(frame33, text=" - Selected SyncMode -> "+tempSyncMode.get())
            
    check_button = tk.Checkbutton(frame33, text="strict", var=tempSyncMode, onvalue="strict", offvalue="smooth", command=syncModeUpdate)
    if(tempSyncMode.get()=="strict"):
        check_button.select()
    else:
        check_button.deselect()
    check_button.pack(side=LEFT)
    tempSyncModeLabel.pack(side=LEFT)

################################################################
### Frame 4/5 - Lower Control Buttons ##########################
################################################################

    frame4 =tk.Frame(win)
    frame4.place(relx=0.05, rely=0.85, relwidth=0.9, relheight=0.05)

    separator = ttk.Separator(frame4, orient='horizontal')
    separator.pack(fill='x')

    frame5 = tk.Frame(win)
    frame5.place(relx=0.05, rely=0.9, relwidth=0.9, relheight=0.1)

    exitBttn = tk.Button(frame5, text="Close", command=win.quit)
#    exitBttn.pack(side=RIGHT)
    exitBttn.place(relx=1.0, rely=0.25, anchor=tk.E)

    def saveConfigWithButton():
        saveConfigData(tempConfigFileName, configFileName)

    saveBttn = tk.Button(frame5, text="Save", command=saveConfigWithButton)
    #saveBttn.pack(side=LEFT)
    saveBttn.place(relx=0.0, rely=0.25, anchor=tk.W)

    def runSync():
#        os.system("SIMPOSYum.exe")
#        import subprocess
#        print(subprocess.call("SIMPOSYum.exe", shell=True))  
        print(os.startfile("SIMPOSYum"))  

    runBttn = tk.Button(frame5, text="Run Sync", command=runSync)
#    runBttn.pack(side=tk.BOTTOM)
    runBttn.place(relx=0.5, rely=0.25, anchor=tk.CENTER)


    win.mainloop()
