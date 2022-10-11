import os
import shutil
import random
import string
import installed_versions

path = installed_versions.minecraftPath
os.chdir(path)

#ask for the world name
worldName = input("What would you like to call your world? Leave blank for 'world': ")
if worldName == "":
    worldName = "world"
#check if the world already exists in the world-stash/saves folder
if os.path.isdir("world-stash/saves/" + worldName):
    print("World already exists. Do you want to replace it? (r) or move it to the inactive folder? (m) or cancel? (c)")
    while True:
        choice = input()
        if choice == "r":
            shutil.rmtree("world-stash/saves/" + worldName)
            break
        elif choice == "m":
            #check if the world already exists in the world-stash/inactive folder
            if os.path.isdir("world-stash/inactive/" + worldName):
                print("World already exists in the inactive folder. Do you want to replace it? (r) or cancel? (c)")
                while True:
                    choice = input()
                    if choice == "r":
                        shutil.rmtree("world-stash/inactive/" + worldName)
                        break
                    elif choice == "c":
                        print("Cancelled")
                        exit()
                    else:
                        print("Invalid choice. Try again.")
            shutil.move("world-stash/saves/" + worldName, "world-stash/inactive/" + worldName)
            break
        elif choice == "c":
            print("Cancelled")
            exit()
        else:
            print("Invalid input. Try again.")

#create the world folder
os.makedirs("world-stash/saves/" + worldName)

#determinate the world seed
print("Do you want a random seed? (r) or filtered seed (f) or enter your own? (o)")
while True:
    choice = input()
    if choice == "r":
        #set seed to a random chracter string
        seed = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation ) for n in range(25)])

        print("Seed: " + seed)
        break
    elif choice == "f":
        print("not implemented yet")
    elif choice == "o":
        seed = input("Enter a seed: ")
        print("Seed: " + seed)
        break
    else:
        print("Invalid input. Try again.")

#ask for backups
print("Do you want to backup your world? (Y/n)")
while True:
    choice = input()
    if choice == "Y":
        backups = True
        break
    elif choice == "n":
        backups = False
        break
    else:
        print("Invalid input. Try again.")

#ask for difficulty
print("Do you want to set the difficulty to peaceful? (p) or easy? (e) or normal? (n) or hard? (h) or hardcore? (hc)")
while True:
    choice = input()
    if choice == "p":
        difficulty = "peaceful"
        break
    elif choice == "e":
        difficulty = "easy"
        break
    elif choice == "n":
        difficulty = "normal"
        break
    elif choice == "h":
        difficulty = "hard"
        break
    elif choice == "hc":
        difficulty = "hardcore"
        break
    else:
        print("Invalid input. Try again.")

#ask for datapacks
print("Do you want to install datapacks? (Y/n)")
while True:
    choice = input()
    if choice == "Y":
        n = 0
        os.makedirs("world-stash/saves/" + worldName + "/datapacks")
        datapacksList = {}
        print("Enter the number of the datapack you want to install, divide with spaces")
        for e in os.listdir("datapacks"):
            n = n + 1
            datapacksList[n] = e
            print (str(n) + ". " + e)      
        datapacks = input()
        datapacks = datapacks.split(" ")
        #check if which number is corrosponding to a datapack
        for e in datapacks:
            for key in datapacksList:
                if e == key:
                   shutil.copy ("datapacks/" + datapacksList[key], "world-stash/saves/" + worldName + "/datapacks/" + datapacksList[key]) 
        break
    elif choice == "n":
        break
    else:
        print("Invalid input. Try again.")

#ask for mods
print("Do you want to install mods? (Y/n)")
while True:
    choice = input()
    if choice == "Y":
        while True:
            print("Fabric (f) or Forge (g)?")
            choice = input()
            if choice == "f":
                modLauncher = "fabric"
                break
            elif choice == "g":
                modLauncher = "forge"
                break
            else:
                modLauncher = "vanilla"
                print("Invalid input. Try again.")
        os.makedirs("world-stash/saves/" + worldName + "/mods")
        modList = {}
        n = 0
        print("Enter the number of the mod you want to install, divide with spaces")
        for e in os.listdir("mods"):
            n = n + 1
            modList[n] = e
            print (str(n) + ". " + e)      
        datapacks = input()
        datapacks = datapacks.split(" ")
        #check if which number is corrosponding to a mod
        for e in datapacks:
            for key in modList:
                if e == key:
                   shutil.copy ("datapacks/" + modList[key], "world-stash/saves/" + worldName + "/mods/" + modList[key]) 
        break
    elif choice == "n":
        break
    else:
        print("Invalid input. Try again.")

#create a file called config.txt in the world folder
configFile = open("world-stash/saves/" + worldName + "/config.txt", "w")
configFile.write("seed=" + seed + "\nbackups=" + str(backups) + "\ndifficulty=" + difficulty + "\nmodLauncher=" + modLauncher + "\nversion=new")
configFile.close()

for e in installed_versions.versions:
    propertiesFile = open("instances/" + e + "/server.properties", "w")
    #serach for the world name in the server.properties file and replace it with the world name
    with open("instances/" + e + "/server.properties") as f:
        for line in f:
            if "level-name" in line:
                line = "level-name=" + worldName + "\n"
            propertiesFile.write(line)
    propertiesFile.close()