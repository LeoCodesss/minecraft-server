import subprocess
import os

mcPath = "/media/ben/LionSSD-Linux/minecraf-server/"
requirements = ["subprocess", "shutil", "random", "string", "re", "fileinput", "os"]

#install requirements if not installed
for requirement in requirements:
    if requirement not in os.listdir("/usr/lib/python3.8/"):
        os.system("sudo pip install " + requirement)

# Make new folders
os.makedirs(mcPath + "datapacks")
os.makedirs(mcPath + "mods")
os.makedirs(mcPath + "world-stash")
os.makedirs(mcPath + "world-stash/saves")
os.makedirs(mcPath + "world-stash/backups")
os.makedirs(mcPath + "world-stash/inactive")
os.makedirs(mcPath + "scripts")
os.makedirs(mcPath + "instances")

# Script Contents

backup = """
import installed_versions
import backupconf
import subprocess
import datetime
import pytz
import re
import schedule
import time
import shutil
import sys

timezone = pytz.timezone(backupconf.timezone)
time = timezone.localize(datetime.datetime.now())

def getScreens():
    screenName = subprocess.run(['screen', '-ls'], stdout=subprocess.PIPE)
    #format "screenName" to only contain the name of all the screens
    screenName = screenName.stdout.decode('utf-8')
    if "No Sockets found in" in screenName:
        return "No screens found"
    screenName = screenName.split('\n')
    #remove the first and last element of the list
    del screenName[0]
    del screenName[-2:]
    screenNameList = []
    for e in screenName:
        e = e.split('\t')
        screenNameList.append(e)
    screenName.clear()
    for e in screenNameList:
        del e[0]
        del e[-2:]
        screenName.append(e)
    screenNameList.clear()
    for o in screenName:
        for e in o:
            for l in range(len(e)):
                if e[l] == '.':
                    e = e[l+1:]
                    break
            screenNameList.append(e)
    return screenNameList

def backup(world, version):
    if backupconf.smartbackups == True:
        subprocess.run(['screen', '-S', e, '-X', 'stuff', 'scoreboard', 'players', 'set', 'count', 'entityCount', '0\n'])
        subprocess.run(['screen', '-S', e, '-X', 'stuff', 'execute', 'as', '@a', 'run', 'scoreboard', 'players', 'add', 'count', 'entityCount', '1\n'])
        subprocess.run(['screen', '-S', e, '-X', 'stuff', 'scoreboard', 'players', 'get', 'count', 'entityCount\n'])
        line = subprocess.check_output(['tail', '-1', installed_versions.minecraftPath + 'instances/' + e + '/screenlog.0']).decode('utf-8')
        for l in line:
            if l.isdigit():
                if not int(l) > 0:
                    subprocess.run(['screen', '-S', version, '-X', 'stuff', 'tellraw', '@a', '{"text":"Backup', 'skipped', 'because',  'no', 'one', 'is', 'online', '(smart', 'backup)","color":"red"}\n'])
                    return
                subprocess.run(['screen', '-S', version, '-X', 'stuff', 'tellraw', '@a', '{"text":"Backup', 'started","color":"green"}\n'])
                #copy folder to backup folder
                #replace [FILENMAE] with the world name
                filename = backupconf.filename.replace('[FILENAME]', world)
                shutil.copytree(installed_versions.minecraftPath + '/world-stash/saves/' + world, installed_versions.minecraftPath + '/world-stash/backups' + filename)
                subprocess.run(['screen', '-S', version, '-X', 'stuff', 'tellraw', '@a', '{"text":"Backup', 'finished","color":"green"}\n'])

def isServerUp():
    screens = getScreens()
    if screens == "No screens found":
        return False
    for v in installed_versions.versions:
        for s in screens:
            if v == s:
                return True
    return False

#check it there is a system argument
if len(sys.argv) > 1:
    if sys.argv[1] == "--now" or sys.argv[1] == "-n":
        backup(sys.argv[2], sys.argv[3])

worldNameDict = {}
#check if a screen session is running
if getScreens() in installed_versions.versions:
    worldNames = []
    screenVersion = []
    for e in getScreens():
        properties = open(installed_versions.minecraftPath + 'instances/' + e + '/server.properties', 'r').close()
        for line in properties:
            if "level-name" in line:
                worldName = line[12:]
                size = len(worldName)
                worldName = worldName[:size - 1]
                worldNames.append(worldName)
                screenVersion.append(e)
                break

count = 0
for e in worldNames:
    config = open(installed_versions.minecraftPath + 'world-stash/saves' + e + 'config.txt', 'r').close()
    for line in config:
        if "backups" in line and "true" in line:
            worldNameDict[e] = True, screenVersion[count]
            break
        else:
            worldNameDict[e] = False, screenVersion[count]

    if True in worldNameDict[e]:
        if backupconf.backuptimeformat == "dynamic":
            #convert h to m
            #check if there is a space in backuptime
            if " " in backupconf.backuptime:
                backuptime = backupconf.backuptime.split(' ')
            else:
                backuptime = [backupconf.backuptime]

            n = 0
            for e in backuptime:
                if re.search('h', e):
                    #search for a number in the string
                    for l in e:
                        if not l.isdigit():
                            #remove the character
                            e = e.replace(l, '')
                            n = int(e) * 60

                elif re.search('m', e):
                    for l in e:
                        if not l.isdigit():
                            e = e.replace(l, '')
                            if n == 0:
                                n = int(e)
                            else:
                                n = int(e) + int(n)

            minutes = n
            #print hi every "minutes" minutes
            
            schedule.every(minutes).minutes.do(backup, e)
    count = count + 1

while isServerUp():
    for e in worldNames:
        if True in worldNameDict[e]:
            if backupconf.backuptimeformat == "dynamic":
                schedule.run_pending()
            elif backupconf.backuptimeformat == "static":
                now = time.hour
                now2 = time.minute
                if len(str(now)) == 1:
                    now = "0" + str(now)
                now2 = datetime.datetime.now().minute
                if len(str(now2)) == 1:
                    now2 = "0" + str(now2)
                now = str(now) + ":" + str(now2)
                backuptimes = backupconf.backuptime.split(' ')
                for t in backuptimes:
                    if now == t:
                        backup(e)
    time.sleep(30)
"""
backupconf = """
#all timezones: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
timezone="Europe/Berlin"

#backuped file name
#"[FILENAME]" will be replaced with the name of the backuped file
#%a: Returns the first three characters of the weekday, e.g. Wed.
#%A: Returns the full name of the weekday, e.g. Wednesday.
#%B: Returns the full name of the month, e.g. September.
#%w: Returns the weekday as a number, from 0 to 6, with Sunday being 0.
#%m: Returns the month as a number, from 01 to 12.
#%p: Returns AM/PM for time.
#%y: Returns the year in two-digit format, that is, without the century. For example, "18" instead of "2018".
#%Y: Returns the year in four-digit format, that is, with the century. For example, "2018" instead of "18".
#%f: Returns microsecond from 000000 to 999999.
#%Z: Returns the timezone.
#%z: Returns UTC offset.
#%j: Returns the number of the day in the year, from 001 to 366.
#%W: Returns the week number of the year, from 00 to 53, with Monday being counted as the first day of the week.
#%U: Returns the week number of the year, from 00 to 53, with Sunday counted as the first day of each week.
#%c: Returns the local date and time version.
#%x: Returns the local version of date.
#+%X: Returns the local version of time.
filename="[FILENAME] %d.%m.%Y %H:%M"

#when to make a backup
#"dynamic" for minutes or hours, "static" for a specific time like 16:30
backuptimeformat="dynamic"
#m for minutes and h for hours, if you are using "static" you can add mulitple times divided by a space
backuptime="1m"

#smart bakups
#when set to true it will only backup if a player is on the server
smartbackups=True
"""
newMcWorld = """
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
"""
startMc = """
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
"""
stopMc = """
import sys
import subprocess
import time
import backup

#check for system arguments
if len(sys.argv) > 1:
    for argv in sys.argv:
        if argv == "backups":
            subprocess.run(['screen', '-S', 'backups', '-X', 'exit\n'])
        else:
            #select the screen using the system argument
            subprocess.run(['screen', '-S', sys.argv[argv], '-X', 'stuff', 'tellraw @a {"text":"Server', 'shutingdown', 'in', '10s"}\n'])
            time.sleep(5)
            subprocess.run(['screen', '-S', sys.argv[argv], '-X', 'stuff', 'tellraw @a {"text":"5"}\n'])
            subprocess.run(['screen', '-S', sys.argv[argv], '-X', 'stuff', 'tellraw @a {"text":"4"}\n'])
            subprocess.run(['screen', '-S', sys.argv[argv], '-X', 'stuff', 'tellraw @a {"text":"3"}\n'])
            subprocess.run(['screen', '-S', sys.argv[argv], '-X', 'stuff', 'tellraw @a {"text":"2"}\n'])
            subprocess.run(['screen', '-S', sys.argv[argv], '-X', 'stuff', 'tellraw @a {"text":"1"}\n'])
            subprocess.run(['screen', '-S', sys.argv[argv], '-X', 'stuff', 'stop\n'])
else:
    print('enter a screen name, leave blank for all')
    screens = input()
    if screens == '':
        allscreens = backup.getScreens()
        for screen in allscreens:
            if screen == "backups":
                subprocess.run(['screen', '-S', 'backups', '-X', 'exit\n'])
            else:
                subprocess.run(['screen', '-S', screen, '-X', 'stuff', 'tellraw @a {"text":"Server', 'shutingdown', 'in', '10s"}\n'])
                time.sleep(5)
                subprocess.run(['screen', '-S', screen, '-X', 'stuff', 'tellraw @a {"text":"5"}\n'])
                subprocess.run(['screen', '-S', screen, '-X', 'stuff', 'tellraw @a {"text":"4"}\n'])
                subprocess.run(['screen', '-S', screen, '-X', 'stuff', 'tellraw @a {"text":"3"}\n'])
                subprocess.run(['screen', '-S', screen, '-X', 'stuff', 'tellraw @a {"text":"2"}\n'])
                subprocess.run(['screen', '-S', screen, '-X', 'stuff', 'tellraw @a {"text":"1"}\n'])
                subprocess.run(['screen', '-S', screen, '-X', 'stuff', 'stop\n'])
"""
uninstallMcVersion = """
import sys
import installed_versions
import os
import shutil

if len(sys.argv) != 2:
    print("Type Mc you want to delete")
    version_input = input()
elif len(sys.argv) == 3:
    version_input = sys.argv[2]
    threesys = True
else:
    version_input = sys.argv[1]

def delete(version, path):
    #remove the version folder and all subfolders
    shutil.rmtree(path)
    #remove from installed_versions.versions
    installed_versions.versions.remove(version)
    print("Delete version: " + version)
    return

print("Warning: This will delete everything in the instances/" + version_input + " folder\ndo you want to continue? (Y/n)")
while True:
    yesNo = input()
    if yesNo == "Y":
        if not version_input in installed_versions.versions:
            print("Version not found\nDo you still want to continue? (Y/n)")
            while True:
                yesNo = input()
                if yesNo == "Y":
                    break
                elif yesNo == "n":
                    print("cancelled")
                    exit()
                else:
                    print("Anser please only Y or n")

        path = installed_versions.minecraftPath + "instances/" +  version_input
        if not os.path.exists(path):
            print("Version not found\nDo you still want to continue? (Y/n)")
            while True:
                yesNo = input()
                if yesNo == "Y":
                    break
                elif yesNo == "n":
                    print("cancelled")
                    exit()
                else:
                    print("Anser please only Y or n")
        
        delete(version_input, path)
        break
    elif yesNo == "n":
        print("cancelled")
        exit()
    else:
        print("please only answer Y or n")
"""
installMcVersion = """
import subprocess
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import sys
import installed_versions
import lxml.html 

#check if there are arguments
if len(sys.argv) != 2:
    print("Type Mc you want to download")
    version_input = input()
else:
    version_input = sys.argv[1]

def writeVer(version):
    with open(installed_versions.minecraftPath + "installed_versions.py", "r") as file:
        #loop through the lines in the file
        newFile = []
        for line in file:
            if "versions" in line:
                oldVersions = installed_versions.versions
                oldVersions.append(version)
                newFile.append("versions=" + str(oldVersions) + "\n")
            else:
                newFile.append(line)
        with open(installed_versions.minecraftPath + "installed_versions.py", "w") as file:
            for line in newFile:
                file.writelines(line)

path = installed_versions.minecraftPath + "instances/" + version_input
urlVa = "https://mcversions.net/download/" + version_input
urlFa = "https://fabricmc.net/use/server/"
for v in installed_versions.versions:
    if version_input == v:
        print(version_input + " is already installed!")
        exit()

#check if the phrase "fabric-" is in version_input
if "fabric-" in version_input:
    request_response = requests.head(urlFa)
    status_code = request_response.status_code
    website_is_up = status_code == 200

    if website_is_up:
        #make the eula
        Path(path).mkdir(parents=True, exist_ok=True)
        with open(path + '/eula.txt', 'w') as f:
            f.write('#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n#Sun Aug 01 21:14:21 CEST 2021\neula=true')
        
        #download the jar
        mcVer = version_input.replace("fabric-", "")
        downloadToPath = path + "/" + version_input +".jar"
        payloadLoader = ""
        payloadInstaller = ""

        loader = requests.request("GET", "https://meta.fabricmc.net/v2/versions/loader", data=payloadLoader)
        installer = requests.request("GET", "https://meta.fabricmc.net/v2/versions/installer", data=payloadInstaller)
        #get the first version of the loader
        loader = loader.json()
        loader = loader[0]
        #get the item with the key "version"
        loader = loader["version"]
        #get the first version of the installer
        installer = installer.json()
        installer = installer[0]
        #get the item with the key "version"
        installer = installer["version"]
        #https://meta.fabricmc.net/v2/versions/loader/1.14/0.14.9/0.11.1/server/jar
        downloadLink = "https://meta.fabricmc.net/v2/versions/loader/" + mcVer + "/" + loader + "/" + installer + "/server/jar"
        #download using "downloadLink" to "downloadToPath"
        with open(downloadToPath, "wb") as file:
            response = requests.get(downloadLink)
            file.write(response.content)

        writeVer(version_input)
        print(version_input + " was successfully installed!")
    else:
        print("Version doesn't exists!")
elif "forge-" in version_input:
    mcVer = version_input.replace("forge-", "")
    #ckeck if the version is smaller than 1.5
    mcVerTmp = mcVer
    if mcVer.count(".") > 1:
        #remove the last dot and everything after it
        mcVerTmp = mcVer[:mcVer.rfind(".")]
    mcVerTmp = mcVerTmp.replace(".", "")

    if int(mcVerTmp) < 15:
            print("Versions below 1.5 are not supported!")
            exit()

    urlFo = "https://files.minecraftforge.net/net/minecraftforge/forge/index_" + mcVer + ".html"
    request_response = requests.head(urlFo)
    status_code = request_response.status_code
    website_is_up = status_code == 200

    if website_is_up:
        #make the eula
        Path(path).mkdir(parents=True, exist_ok=True)
        with open(path + '/eula.txt', 'w') as f:
            f.write('#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n#Sun Aug 01 21:14:21 CEST 2021\neula=true')
        
        #download the site
        downloadToPath = path + "/" + version_input +".jar"
        result = requests.get(urlFo)
        doc = lxml.html.fromstring(result.text)
        #ckeck if the element with the xpath exists
        if doc.xpath("/html/body/main/div[2]/div[1]/div[2]/div/div[2]/div[1]/small"):
            forgeVersion = doc.xpath("/html/body/main/div[2]/div[1]/div[2]/div/div[2]/div[1]/small")[0].text
        else:
            forgeVersion = doc.xpath("/html/body/main/div[2]/div[1]/div[2]/div/div/div[1]/small")[0].text
        
        #forgeVersion = forgeVersion.replace(mcVer + " - ", "")
        downloadLink = "https://maven.minecraftforge.net/net/minecraftforge/forge/" + forgeVersion + "/forge-" + forgeVersion + "-installer.jar"
        download = requests.get(downloadLink)
        open(downloadToPath, "wb").write(download.content)
        subprocess.run(["java", "-jar", downloadToPath, "--installServer"])
        writeVer(version_input)
        print(version_input + " was successfully installed!")
    else:
        print("Version doesn't exists!")
else:
    request_response = requests.head(urlVa)
    status_code = request_response.status_code
    website_is_up = status_code == 200


    if website_is_up:
        #make a folder called version_input
        Path(path).mkdir(parents=True, exist_ok=True)
        with open(path + '/eula.txt', 'w') as f:
            f.write('#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n#Sun Aug 01 21:14:21 CEST 2021\neula=true')       
        result = requests.get(urlVa).content
        doc = BeautifulSoup(result, 'html.parser')
        link = doc.find("a", {"class": "text-xs whitespace-nowrap py-3 px-8 bg-green-700 hover:bg-green-900 rounded text-white no-underline font-bold transition-colors duration-200"})
        downloadPath = path + "/" + version_input + ".jar"
        download = requests.get(link['href'])
        open(downloadPath, "wb").write(download.content)
        #version_input to installed_versions.versions
        writeVer(version_input)
        print(version_input + " was successfully installed")
    else:
        print("Version doesn't exists!")
"""
config = """
versions = []
minecraftPath = "/minecraft-server/"
"""
