import subprocess
import sys
import os
import re
import installed_versions

#check if there is a sys.argv[1]
if len(sys.argv) == 2:
    inputVersion = sys.argv[1]
else:
    inputVersion = input("Enter the version you want to start: ")

os.chdir(installed_versions.minecraftPath)

if inputVersion in installed_versions.versions:
    os.chdir(installed_versions.minecraftPath + inputVersion)
    #ask if the user wants to select a spefic world
    properties = open(installed_versions.minecraftPath + inputVersion + "/server.properties", "r")
    for line in properties:
        if re.search("level-name=", line):
            worldName = line[11:]
            size = len(worldName)
            worldName = worldName[:size - 1]

    print("Do you want to select a spefic world? (s) or create a new one? (n) or use current world: " + worldName + " (c or leave blank)")
    while True:
        yesNo = input()
        if yesNo == "s":
            n = 0
            worlds = []
            print("Select a world: ")
            for world in os.listdir(installed_versions.minecraftPath + "world-stash/saves"):
                n = n + 1
                worlds.append(world)
                print(n + ". " + world)
            while True:
                worldNumber = input()
                if worldNumber.isdigit():
                    worldNumber = int(worldNumber)
                    if worldNumber > n:
                        print("World doesn't exist")
                    else:
                        selectedWorld = worlds[worldNumber - 1]
                        print("Selected world: " + selectedWorld)
                        break
                else:
                    print("Please enter a number")
            break
        elif yesNo == "n":
            #ececute the newMcWorld.py command
            subprocess.run(['python3.10', 'newMcWorld.py'])
            break
        elif yesNo == "c":
            print("Using current world " + worldName)
            break
        else:
            print("please only anser s, n or c")

    configLoc = "world-stash/saves" + worldName + "/config.txt"
    config = open(configLoc, "r")
    for line in config:
        if re.search("version", line):
            version = line[8:]
            size = len(version)
            version = version[:size - 1]
    if version == inputVersion or version == "new":
        print("Starting world " + worldName)
    else:
        print("This world was last startet in " + version + " do you want to continue? (Y/n)")
        while True:
            yesNo = input()
            if yesNo == "Y":
                print("Starting world " + worldName)
                break
            elif yesNo == "n":
                print("Start cancelled")
                exit()
            else:
                print("Anser please only Y or n")
    
    #write server properties

    with open(configLoc, "r") as file:
        configLines = file.readlines()
        for lines in configLines:
            if re.search("seed", lines):
                seed = lines[5:]
                size = len(seed)
                seed = seed[:size - 1]
            elif re.search("difficulty", lines):
                difficulty = lines[11:]
                size = len(difficulty)
                difficulty = difficulty[:size - 1]
                
                

    for e in installed_versions.versions:
        propertiesFile = open("instances/" + e + "/server.properties", "w")
        #serach for the world name in the server.properties file and replace it with the world name
        with open("instances/" + e + "/server.properties") as f:
            for line in f:
                if "level-name" in line:
                    line = "level-name=" + worldName + "\n"
                elif "level-seed" in line:
                    line = "level-seed=" + seed + "\n"
                elif difficulty == "hardcore":
                    if "hardcore" in line:
                        line = "hardcore=true\n"
                    if "difficulty" in line:
                        line = "difficulty=hard\n"
                else:
                    if "hardcore" in line:
                        line = "hardcore=false\n"
                    if "difficulty" in line:
                        line = "difficulty=" + difficulty + "\n"

                propertiesFile.write(line)
        propertiesFile.close()

    subprocess.run(['screen', '-m', '-d', '-L', '-S', inputVersion, 'sudo', 'java', '-Xms1024M', '-Xmx8024M', '-jar', installed_versions.minecraftPath + inputVersion + '/' + inputVersion + '.jar', '--nogui'])
    subprocess.run(['screen', '-m', 'd', '-S', 'backups', 'python3.10', 'backup.py'])

else:
    print(inputVersion + " isn't installed!")