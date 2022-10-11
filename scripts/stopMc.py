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