#!/usr/bin/env python3

import tkinter as tk
from tkinter import LEFT, RIGHT, ttk
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
        configTemp = Setup.SetupData()
        configTemp.load(tempConfigFileName)
        configTemp.SrcDir = selectedSrcPath
        configTemp.save(tempConfigFileName)
        tempSrcFolderLabel.config(text = selectedSrcPath)

    def getDestFolderPath():
        selectedDestPath = str(filedialog.askdirectory())
        print("selectedDestPath: "+selectedDestPath)
        configTemp = Setup.SetupData()
        configTemp.load(tempConfigFileName)
        configTemp.DestDir = selectedDestPath
        configTemp.save(tempConfigFileName)
        tempDestFolderLabel.config(text = selectedDestPath)

    def syncModeUpdate():
        configTemp = Setup.SetupData()
        configTemp.load(tempConfigFileName)
        configTemp.SyncMode = tempSyncMode.get()
        configTemp.save(tempConfigFileName)
        modeStatusLabel.config(text="Current SyncMode: "+tempSyncMode.get())
        
    def saveConfigData(SrcFile, DestFile):
        ret = copyFile_save(SrcFile, DestFile)
        if(ret == 'OK'):
           messagebox.showinfo("Config saved successfully")
        else:
            messagebox.showerror("Save config file error", ret)

    winHide("SIMPOSYum_SetupGui.exe")

    config = Setup.SetupData()
    config.load(configFileName)

    ret = copyFile_save(configFileName, tempConfigFileName)
    if(ret != 'OK'):
        messagebox.showerror("File save error", ret)

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
    modeLabel = tk.Label(frame3, text= 'Synchronisation mode: ')
    modeLabel.pack(side=LEFT)

    frame33 = tk.Frame(win)
    frame33.place(relx=0.05, rely=0.55, relwidth=0.9, relheight=0.15)

    tempSyncMode = tk.StringVar(frame33, config.SyncMode)
    modeStatusLabel = tk.Label(frame33, text="Current SyncMode: "+tempSyncMode.get())
            
    check_button = tk.Checkbutton(frame33, text="strict", var=tempSyncMode, onvalue="strict", offvalue="smooth", command=syncModeUpdate)
    if(tempSyncMode.get()=="strict"):
        check_button.select()
    else:
        check_button.deselect()
    check_button.pack(side=LEFT)
    modeStatusLabel.pack(side=RIGHT)

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
    exitBttn.pack(side=RIGHT)

    def saveConfigWithButton():
        saveConfigData(tempConfigFileName, configFileName)

    saveBttn = tk.Button(frame5, text="Save", command=saveConfigWithButton)
    saveBttn.pack(side=LEFT)

    win.mainloop()
