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

# set the mcPath in the config file
with open(mcPath + "scripts/installed_vesions.py", "r") as f:
    lines = f.readlines()
    lines[0] = "mcPath = '" + mcPath + "'\n"
with open(mcPath + "scripts/installed_vesions.py", "w") as f:
    f.writelines(lines)