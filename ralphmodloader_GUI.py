import os, zipfile, shutil, glob, time
import tkinter as tk
import webbrowser
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from distutils.dir_util import copy_tree
from sys import platform, argv
from tkinter.messagebox import showerror, showwarning, showinfo, askyesno
import argparse

""" parser = argparse.ArgumentParser()
opt1 = parser.add_argument('-v', '--verbose', action='store_true')

args = parser.parse_args(opt1)

args = parser.parse_args()
print(args.accumulate(args.integers)) """

#########
#VERSION#
#########
ver = "Ralph Mod Loader GUI 1.3"
print(ver)

root = tk.Tk()
root.title(ver)
root.geometry('300x200')
root.resizable(False, False)
root.tk.call("source", "azure.tcl")

if platform == "linux" or platform == "linux2":
    root.tk.call("set_theme", "light")
    print("Light theme has been enabled since the dark one has issues with Linux.")
    gameDefDir = "~/.steam/steam/steamapps/common/Ralph's party RPG"
elif platform == "win32":
    root.tk.call("set_theme", "dark")
    if os.path.exists("C:/Program Files/Steam/steamapps/common/Ralph's party RPG"):
        gameDefDir = "C:/Program Files/Steam/steamapps/common/Ralph's party RPG"
    else:
        root.tk.call("set_theme", "light")
        gameDefDir = "C:/Program Files (x86)/Steam/steamapps/common/Ralph's party RPG"
else:
    print("WARNING:")
    print("Your platform might be incompatible with this program.")
zipDefDir = "~/Downloads/"

def launchGame():
    webbrowser.open('steam://rungameid/1977230')

def installMod():
    print("Select the mod you want to install (should be a .ralph or a .zip file)")
    showinfo("Select a mod", "Select a .ralph or a .zip mod file you want to install.")
    filetypes = (
        ('.ralph mods', '*.ralph'),
        ('.zip mods', '*.zip'),
        ('All files', '*.*'),
    )

    tk.Tk().withdraw()
    fn = askopenfilename(
        title='Select a mod installation file...',
        filetypes=filetypes,
        initialdir=zipDefDir,
    )
    if not ".zip" or not ".ralph" in fn:
        showerror("Canceled", "You canceled the installation.")
        exit()
    zip = zipfile.ZipFile(fn)
    try:
        ralfmod = zip.open("Ralph's party RPG/Data/System.rvdata")
        zipSubfolder = 1
    except KeyError:
        try:
            ralfmod = zip.open("Data/System.rvdata")
            zipSubfolder = 0
        except KeyError:
            print("---------------------------------------")
            print("ERROR:")
            print("This zip isn't a Ralph's Party RPG mod.")
            print("---------------------------------------")
            showerror("ERROR!", "This zip isn't a Ralph's Party RPG mod.")
            exit()
    print(" ")
    print("---------------------------------------")
    print("Selected", fn)
    cModSel = askyesno(" ", "Selected " + fn + ". Is this okay?")
    if cModSel == True:
        showinfo(" ", "Continuing...")
    else:
        showinfo(" ", "Stopping...")
        exit()
    print("Choose the Ralph's Party RPG install directory")
    showinfo("Install directory", "Choose the Ralph's Party RPG install directory")
    tk.Tk().withdraw()
    ralphdir = askdirectory(
        title='Select Ralphs Party RPG install directory...',
        initialdir=gameDefDir,
    )
    if not "/" in ralphdir:
        print("Stopping...")
        showinfo(" ", "Stopping...")
        exit()
    print(" ")
    print("---------------------------------------")
    print("Selected", ralphdir)
    print("Is this okay?")
    instDirQues = askyesno("Selected directory", "Selected " + ralphdir + ". Is this okay?")
    if instDirQues == True:
        print("Continuing...")
        showinfo(" ", "Continuing...")
    else:
        print("Stopping...")
        showinfo(" ", "Stopping...")
        exit()

    installCheck = ralphdir + "/Game.exe"
    if not os.path.exists(installCheck):
        print("---------------------------------------")
        print("ERROR:")
        print("Ralph's party RPG isn't installed here!")
        print("---------------------------------------")
        showerror("ERROR!", "Ralph's Party RPG isn't installed here!")
        exit()
    subFolderInstall = ralphdir + "/Ralph's party RPG/"
    backupFilesPath = ralphdir + "/original/"
    ralphdir = ralphdir + "/"
    if os.path.exists(backupFilesPath):
        print("-------------------------------------------")
        print("ERROR:")
        print("Uninstall the mod you currently have first.")
        print("-------------------------------------------")
        showerror("ERROR!", "Uninstall the mod you currently have first.")
        exit()
    print("Backing up the original files...")
    shutil.copytree(ralphdir, backupFilesPath)
    print("Successfully backed up the original files")
    print("Extracting the mod files...")
    with zipfile.ZipFile(fn, 'r') as zip_ref:
        zip_ref.extractall(ralphdir)
    if zipSubfolder == 1:
        print("Subfolder detected! Changing a few things...")
        copy_tree(subFolderInstall, ralphdir)
        shutil.rmtree(subFolderInstall)
    print("Successfully installed the mod!")
    if platform == "win32":
        askLaunch = askyesno("Success!", "Successfully installed the mod! Do you want to launch the game?")
        if askLaunch == True:
            launchGame()
    else: showinfo("Success!", "Successfully installed the mod!")
    exit()

def uninstallMod():
    print("Choose the Ralph's Party RPG install directory.")
    showinfo("Install directory", "Choose the Ralph's Party RPG install directory")
    tk.Tk().withdraw()
    ralphdir = askdirectory(
        title='Select Ralphs Party RPG install directory...',
        initialdir=gameDefDir,
    )
    if not "/" in ralphdir:
        print("Stopping...")
        showerror("Canceled", "You canceled the uninstallation.")
        exit()
    print(" ")
    print("---------------------------------------")
    print("Selected", ralphdir)
    print("Is this okay?")
    instDirQues = askyesno("", "Selected " + ralphdir + ". Is this okay?")
    if instDirQues == True:
        print("Continuing...")
        showinfo(" ", "Continuing...")
    else:
        print("Stopping...")
        showinfo(" ", "Stopping...")
        exit()

    installCheck = ralphdir + "/original"
    if not os.path.exists(installCheck):
        print("------------------------------------")
        print("ERROR:")
        print("Ralph's party RPG isn't modded here!")
        print("------------------------------------")
        showerror("ERROR!", "Ralph's Party RPG isn't modded here!")
        exit()

    os.chdir(ralphdir)
    retain = "original"
    print("Uninstalling the mod...")
    for item in os.listdir(os.getcwd()):
        if item not in retain:
            try:
                os.remove(item)
            except IsADirectoryError:
                shutil.rmtree(item)
      
    print("Successfully uninstalled the mod")
    print("Restoring the original game...")
    shutil.copytree(installCheck, ralphdir, dirs_exist_ok = True)
    print("Successfully restored the original game")
    print("Cleaning up...")
    shutil.rmtree(installCheck)
    print("All done!")
    if platform == "win32":
        askLaunch = askyesno("Success!", "Successfully uninstalled the mod and restored the original game! Do you want to launch the game?")
        if askLaunch == True:
            launchGame()
    else: showinfo("Success!", "Successfully uninstalled the mod and restored the original game!")
    exit()
if platform == "win32":
    installChoice = ttk.Button(
        root, text="Install a mod", command=installMod, style="Accent.TButton"
    )
    uninstallChoice = ttk.Button(
        root, text="Uninstall a mod", command=uninstallMod, style="Accent.TButton"
    )
else:
    installChoice = ttk.Button(
        root, text="Install a mod", command=installMod
    )
    uninstallChoice = ttk.Button(
        root, text="Uninstall a mod", command=uninstallMod
    )

installChoice.pack(
    ipadx=5, ipady=5, expand=True, side="left"
)
uninstallChoice.pack(
    side="right", expand=True, ipadx=5, ipady=5
)


root.mainloop()