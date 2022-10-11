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
