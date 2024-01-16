import os, sys, hashlib

def banner(appVersion):
    print(f"""\033[93m
           _____            _____                    _____                    _____                    _____                    _____                    _____          
          /\    \          /\    \                  /\    \                  /\    \                  /\    \                  /\    \                  /\    \         
         /::\____\        /::\    \                /::\____\                /::\____\                /::\    \                /::\    \                /::\    \        
        /:::/    /        \:::\    \              /::::|   |               /:::/    /               /::::\    \              /::::\    \              /::::\    \       
       /:::/    /          \:::\    \            /:::::|   |              /:::/    /               /::::::\    \            /::::::\    \            /::::::\    \      
      /:::/    /            \:::\    \          /::::::|   |             /:::/    /               /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \     
     /:::/    /              \:::\    \        /:::/|::|   |            /:::/____/               /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \    
    /:::/    /               /::::\    \      /:::/ |::|   |           /::::\    \              /::::\   \:::\    \      /::::\   \:::\    \      /::::\   \:::\    \   
   /:::/    /       ____    /::::::\    \    /:::/  |::|   | _____    /::::::\____\________    /::::::\   \:::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \  
  /:::/    /       /\   \  /:::/\:::\    \  /:::/   |::|   |/\    \  /:::/\:::::::::::\    \  /:::/\:::\   \:::\    \  /:::/\:::\   \:::\____\  /:::/\:::\   \:::\____\ 
 /:::/____/       /::\   \/:::/  \:::\____\/:: /    |::|   /::\____\/:::/  |:::::::::::\____\/:::/  \:::\   \:::\____\/:::/  \:::\   \:::|    |/:::/  \:::\   \:::|    |
 \:::\    \       \:::\  /:::/    \::/    /\::/    /|::|  /:::/    /\::/   |::|~~~|~~~~~     \::/    \:::\  /:::/    /\::/    \:::\  /:::|____|\::/    \:::\  /:::|____|
  \:::\    \       \:::\/:::/    / \/____/  \/____/ |::| /:::/    /  \/____|::|   |           \/____/ \:::\/:::/    /  \/_____/\:::\/:::/    /  \/_____/\:::\/:::/    / 
   \:::\    \       \::::::/    /                   |::|/:::/    /         |::|   |                    \::::::/    /            \::::::/    /            \::::::/    /  
    \:::\    \       \::::/____/                    |::::::/    /          |::|   |                     \::::/    /              \::::/    /              \::::/    /   
     \:::\    \       \:::\    \                    |:::::/    /           |::|   |                     /:::/    /                \::/____/                \::/____/    
      \:::\    \       \:::\    \                   |::::/    /            |::|   |                    /:::/    /                  ~~                       ~~          
       \:::\    \       \:::\    \                  /:::/    /             |::|   |                   /:::/    /                                                        
        \:::\____\       \:::\____\                /:::/    /              \::|   |                  /:::/    /                    \033[0m\033[94mv{appVersion}\033[0m\033[93m                                 
         \::/    /        \::/    /                \::/    /                \:|   |                  \::/    /                                                          
          \/____/          \/____/                  \/____/                  \|___|                   \/____/                                                           
\033[0m""")

def correctFormat(txt):
    return all([char.isdigit() or char.isalpha() for char in txt])


os.system("mode con cols=169 lines=35")

appVersion = "1.0"

banner(appVersion)
print("\n\n")


dirAppExec = os.path.join(os.getenv('USERPROFILE'), os.getenv('HOMEPATH'), "Desktop")
dirApp = os.path.join(os.getenv('HOMEDRIVE'), "\\LinkApp")

print(f" The program will install LinkApp in the following directory: \033[93m{dirApp}\033[0m")

dirOrigin = f"{os.getcwd()}\\assets\\"
dirDestination = f"{dirApp}\\assets\\"

os.system(f"if not exist {dirApp} mkdir {dirApp}")
os.system(f"if not exist {dirDestination} mkdir {dirDestination}")

if "img" not in os.listdir(dirDestination):
    os.system(f"xcopy \"{dirOrigin}\" \"{dirDestination}\" /E /C /Q /K /Y > nul")

dirDestination = f"{dirApp}\\"

if "installer.bat" not in os.listdir(dirDestination):
    dirOrigin = f"{os.getcwd()}\\installer.bat"
    os.system(f"xcopy \"{dirOrigin}\" \"{dirApp}\" /C /Q /K /Y > nul")

if "installer.py" not in os.listdir(dirDestination):
    dirOrigin = f"{os.getcwd()}\\installer.py"
    os.system(f"xcopy \"{dirOrigin}\" \"{dirDestination}\" /C /Q /K /Y > nul")

if "main.py" not in os.listdir(dirDestination):
    dirOrigin = f"{os.getcwd()}\\main.py"
    os.system(f"xcopy \"{dirOrigin}\" \"{dirDestination}\" /C /Q /K /Y > nul")


os.system(f"type nul>\"{dirAppExec}\LinkApp.bat\"")
os.system(f"echo @echo off>>\"{dirAppExec}\LinkApp.bat\"")
os.system(f"echo title LinkApp v{appVersion}>>\"{dirAppExec}\LinkApp.bat\"")
os.system(f"echo cd {dirApp}>>\"{dirAppExec}\LinkApp.bat\"")
os.system(f"echo python {dirApp}\main.py>>\"{dirAppExec}\LinkApp.bat\"")

os.chdir(dirApp)

print(f"\033[92m LinkApp v{appVersion} was added to the Desktop\033[0m")


print()

print("\033[95m Click any key to start fetching the libraries required...\033[0m")
os.system("pause > nul")

try:
    from progress.bar import Bar

except ImportError:
    os.system("pip install progress")
    from progress.bar import Bar



librariesBar = Bar(" LinkApp required libraries", fill="#", max=3, suffix="%(percent)d%%")

try:
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtWidgets import QMessageBox

except ImportError:
    os.system("pip install pyqt5")

librariesBar.next()

try:
    import requests

except ImportError:
    os.system("pip install requests")

librariesBar.next()

try:
    import pyperclip

except ImportError:
    os.system("pip install pyperclip")

librariesBar.next()
librariesBar.finish()

createCredentials = False
filesBar = Bar(" LinkApp required files    ", fill="#", max=4, suffix="%(percent)d%%")

if "links.txt" not in os.listdir():
    with open("links.txt", "w") as f:
        f.write("")
filesBar.next()

if "theme.txt" not in os.listdir():
    with open("theme.txt", "w") as f:
        f.write("0")
filesBar.next()

if "username.txt" not in os.listdir():
    with open("username.txt", "w") as f:
        f.write("")

    createCredentials = True
filesBar.next()

if "password.txt" not in os.listdir():
    with open("password.txt", "w") as f:
        f.write("")

    createCredentials = True
filesBar.next()

filesBar.finish()


if librariesBar.progress == 1 and filesBar.progress == 1:
    if createCredentials:
        print("\033[95m Click any key to continue...\033[0m")
        os.system("pause > nul")

    else:
        print(f"\033[92m LinkApp v{appVersion} was successfully installed in {dirApp}\033[0m")
        print("\033[95m Click any key to close...\033[0m")
        os.system("pause > nul")
        sys.exit(1)

else:
    print(f"\033[51m\n Unable to install LinkApp v{appVersion}\033[0m")
    os.system("pause > nul")
    sys.exit(1)

os.system("cls")
banner(appVersion)
print("\n\n")

username = input(" Write your username for LinkApp: ")
while not correctFormat(username):
    print(" You can only use alphanumerical characters")
    username = input(" Write your username for LinkApp: ")

password = input(f" Write your password for {username}: ")
while not correctFormat(password):
    print(" You can only use alphanumerical characters")
    password = input(f" Write your password for {username}: ")

print()
credentialsBar = Bar(" Hashing credentials      ", fill="#", max=2, suffix="%(percent)d%%")

with open("username.txt", "w") as f:
    f.write(hashlib.sha256(username.encode()).hexdigest())
credentialsBar.next()

with open("password.txt", "w") as f:
    f.write(hashlib.sha256(password.encode()).hexdigest())
credentialsBar.next()
credentialsBar.finish()

print(f"\033[92m\n Credentials successfully created for {username}\033[0m")
print(f"\033[92m LinkApp v{appVersion} was successfully installed in {dirApp}\033[0m")
print("\033[95m Click any key to close...\033[0m")
os.system("pause > nul")
