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
                

