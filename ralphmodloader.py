import os, zipfile, shutil, glob, time
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from distutils.dir_util import copy_tree
from sys import platform

print("RalphModLoader v1.2.1")
if platform == "linux" or platform == "linux2":
    gameDefDir = "~/.steam/steam/steamapps/common/Ralph's party RPG"
elif platform == "win32":
    if os.path.exists("C:/Program Files/Steam/steamapps/common/Ralph's party RPG"):
        gameDefDir = "C:/Program Files/Steam/steamapps/common/Ralph's party RPG"
    else:
        gameDefDir = "C:/Program Files (x86)/Steam/steamapps/common/Ralph's party RPG"
else:
    print("WARNING:")
    print("Your platform might be incompatible with this program.")
zipDefDir = "~/Downloads/"
print("")
print("Do you want to install (1) or uninstall (2) a mod?")
try:
    uninChoice = int(input("Enter either 1 or 2: "))
except ValueError:
    print("--------------------")
    print("ERROR:")
    print("Enter either 1 or 2.")
    print("--------------------")
    exit()
if uninChoice == 1:
    print("Select the mod you want to install (should be a .ralph or a .zip file)")

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
        print("Stopping...")
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
            exit()
    print(" ")
    print("---------------------------------------")
    print("Selected", fn)
    print("Is this okay? (y/n)")
    yn = input("")
    if yn == "y" or yn == "Y" or yn == "yes" or yn == "Yes" or yn == "YES":
        print("Continuing...")
    else:
        print("Stopping...")
        exit()

    print("Choose the Ralph's Party RPG install directory")
    tk.Tk().withdraw()
    ralphdir = askdirectory(
        title='Select Ralphs Party RPG install directory...',
        initialdir=gameDefDir,
    )
    if not "/" in ralphdir:
        print("Stopping...")
        exit()
    print(" ")
    print("---------------------------------------")
    print("Selected", ralphdir)
    print("Is this okay? (y/n)")
    yn = input("")
    if yn == ("y" or "Y" or "yes" or "Yes" or "YES"):
        print("Continuing...")
    else:
        print("Stopping...")
        exit()

    installCheck = ralphdir + "/Game.exe"
    if not os.path.exists(installCheck):
        print("---------------------------------------")
        print("ERROR:")
        print("Ralph's party RPG isn't installed here!")
        print("---------------------------------------")
        exit()
    subFolderInstall = ralphdir + "/Ralph's party RPG/"
    backupFilesPath = ralphdir + "/original/"
    ralphdir = ralphdir + "/"
    if os.path.exists(backupFilesPath):
        print("-------------------------------------------")
        print("ERROR:")
        print("Uninstall the mod you currently have first.")
        print("-------------------------------------------")
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



elif uninChoice == 2:
    print("Choose the Ralph's Party RPG install directory")
    tk.Tk().withdraw()
    ralphdir = askdirectory(
        title='Select Ralphs Party RPG install directory...',
        initialdir=gameDefDir,
    )
    if not "/" in ralphdir:
        print("Stopping...")
        exit()
    print(" ")
    print("---------------------------------------")
    print("Selected", ralphdir)
    print("Is this okay? (y/n)")
    yn = input("")
    if yn == "y" or yn == "Y" or yn == "yes" or yn == "Yes" or yn == "YES":
        print("Continuing...")
    else:
        print("Stopping...")
        exit()

    installCheck = ralphdir + "/original"
    if not os.path.exists(installCheck):
        print("------------------------------------")
        print("ERROR:")
        print("Ralph's party RPG isn't modded here!")
        print("------------------------------------")
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
    

else:
    print("--------------------")
    print("ERROR:")
    print("Enter either 1 or 2.")
    print("--------------------")
    exit()