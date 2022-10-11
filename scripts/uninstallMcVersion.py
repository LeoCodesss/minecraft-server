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