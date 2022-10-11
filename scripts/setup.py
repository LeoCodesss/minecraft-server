import subprocess
import os

#set mcPath to current directory
mcPath = os.getcwd()

# Make new folders
os.makedirs(mcPath + "datapacks")
os.makedirs(mcPath + "mods")
os.makedirs(mcPath + "world-stash")
os.makedirs(mcPath + "world-stash/saves")
os.makedirs(mcPath + "world-stash/backups")
os.makedirs(mcPath + "world-stash/inactive")
os.makedirs(mcPath + "scripts")
os.makedirs(mcPath + "instances")
