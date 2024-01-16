import os, sys, json, webbrowser, hashlib

try:
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtWidgets import QMessageBox
    import requests, pyperclip

except ImportError:
    print("Warning: Fail while uploading libraries. Execute the installer.")
    os.system("pause > nul")
    sys.exit(1)

def is_wifi():
    '''
    Returns True if the wifi is active
    '''
    
    try:
        r = requests.get('https://google.com')
        return True

    except:
        return False

class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setWindowIcon(QtGui.QIcon("assets/img/LinkApp.ico"))

        self.linkId2Del = 0
        self.linkObj2Del = 0
        self.links = self.getLinks()
        self.linksFav = []
        self.linksObj = []

        self.setScaledImg = False
        self.appMenu = 'home'
        self.msgText = None
        self.changeUserState = True
        self.changePasswordState = True

        with open('theme.txt', 'r') as f:
            self.themeCol = f.read()
            if self.themeCol.isdigit():
                self.themeCol = int(self.themeCol)
                if self.themeCol > 1:
                    self.themeCol = 2

                elif self.themeCol < 1:
                    self.themeCol = 0

                else:
                    self.themeCol = 1

            else:
                self.themeCol = 0

        # We apply the corresponding theme color
        if self.themeCol > 1:
            self.setThemeDark(self.computerTheme())
        
        else:
            self.setThemeDark(bool(self.themeCol))

        # Fonts configuration
        self.font10 = QtGui.QFont()
        self.font10.setFamily("Calibri")
        self.font10.setPointSize(10)

        self.font12 = QtGui.QFont()
        self.font12.setFamily("Calibri")
        self.font12.setPointSize(12)

        self.font14 = QtGui.QFont()
        self.font14.setFamily("Calibri light")
        self.font14.setPointSize(14)

        self.fontCal10BW75 = QtGui.QFont()
        self.fontCal10BW75.setFamily("Calibri")
        self.fontCal10BW75.setPointSize(10)
        self.fontCal10BW75.setBold(True)
        self.fontCal10BW75.setWeight(75)

        self.fontD9BW75 = QtGui.QFont()
        self.fontD9BW75.setPointSize(9)
        self.fontD9BW75.setBold(True)
        self.fontD9BW75.setWeight(75)

    def loginUI(self):
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.setWindowTitle("LinkApp")

        self.loginCentralWidget = QtWidgets.QWidget(self.MainWindow)
        self.loginCentralWidget.setObjectName("loginCentralWidget")

        self.MainWindow.setCentralWidget(self.loginCentralWidget)
        self.MainWindow.setFixedSize(450, 440)
        self.MainWindow.setStyleSheet("QMainWindow{" + f"{self.MainWinCol}" + "}" + 'QScrollBar:vertical {' + f'background-color: rgb({self.themeBackQScrollBar});' + 'min-width: 20px;margin: 21px 0 21px 0;}QScrollBar::handle:vertical {' + f'background-color: rgb({self.themeQScrollBar});' + 'min-height: 25px;}QScrollBar::add-line:vertical {' + f"background-color: rgb({self.themeQScrollBarBox});" + "height: 20px;subcontrol-position: bottom;subcontrol-origin: margin;}QScrollBar::sub-line:vertical {" + f"background-color: rgb({self.themeQScrollBarBox});" + "height: 20px;subcontrol-position: top;subcontrol-origin: margin;}QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: none;}")

        self.loginTries = 3

        self.userEntered = QtWidgets.QLineEdit(self.loginCentralWidget)
        self.userEntered.setGeometry(QtCore.QRect(53, 150, 344, 52))
        self.userEntered.setFont(self.font14)
        self.userEntered.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.userEntered.setObjectName("userEntered")
        self.userEntered.setClearButtonEnabled(True)
        self.userEntered.setPlaceholderText(" Introduce your username")
        self.userEntered.setStyleSheet("border:none;border-radius:3px;" + f"background-color:rgb({self.themeLineEdit});color:rgb({self.themeColLet_tb});")

        self.passEntered = QtWidgets.QLineEdit(self.loginCentralWidget)
        self.passEntered.setGeometry(QtCore.QRect(53, 220, 344, 52))
        self.passEntered.setFont(self.font14)
        self.passEntered.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passEntered.setObjectName("passEntered")
        self.passEntered.setClearButtonEnabled(True)
        self.passEntered.setPlaceholderText(" Introduce your password")
        self.passEntered.setStyleSheet("border:none;border-radius:3px;" + f"background-color:rgb({self.themeLineEdit});color:rgb({self.themeColLet_tb});")

        self.btnEnter = QtWidgets.QPushButton(self.loginCentralWidget)
        self.btnEnter.setGeometry(QtCore.QRect(53, 320, 344, 52))
        self.btnEnter.setFont(self.font14)
        self.btnEnter.setText("Enter")
        self.btnEnter.setObjectName("btnEnter")
        self.btnEnter.setStyleSheet("QPushButton#btnEnter{color:#fff;border:none;background-color:rgb(88, 101, 242);border-radius:5px;}QPushButton#btnEnter:hover{background-color:rgb(71, 82, 196)}")

        self.loginImg = QtWidgets.QLabel(self.loginCentralWidget)
        self.loginImg.setGeometry(QtCore.QRect(53, 50, 344, 59))
        self.loginImg.setMaximumSize(QtCore.QSize(344, 59))
        self.loginImg.setPixmap(QtGui.QPixmap("assets/img/LinkApp.png"))
        self.loginImg.setScaledContents(False)
        self.loginImg.setObjectName("loginImg")


        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)


        self.passEntered.returnPressed.connect(self.loginCheckCredentials)
        self.btnEnter.clicked.connect(self.loginCheckCredentials)

    def loginCheckCredentials(self):
        usEncoded = hashlib.sha256(self.userEntered.text().encode()).hexdigest()
        passEncoded = hashlib.sha256(self.passEntered.text().encode()).hexdigest()

        dirApp = os.path.join(os.getenv('HOMEDRIVE'), "\\LinkApp")
        os.chdir(dirApp)

        with open("username.txt") as f:
            usReal = f.readline()

        with open("password.txt") as f:
            passReal = f.readline()

        if usEncoded == usReal and passEncoded == passReal:
            self.username = self.userEntered.text()
            self.setupUi()

        else:
            self.loginTries -= 1
            self.btnEnter.setText(f"Incorrect: {self.loginTries} remaining")
            self.btnEnter.setStyleSheet("QPushButton#btnEnter{color:#fff;border:none;background-color:rgb(242, 63, 66);border-radius:5px;}QPushButton#btnEnter:hover{background-color:rgb(161, 40, 40)}")
            
            if self.loginTries == 0:
                sys.exit(2)

    def setupUi(self):
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.setWindowTitle("LinkApp")
        self.MainWindow.setFixedSize(776, 623)

        self.mainCentralWidget = QtWidgets.QWidget(self.MainWindow)
        self.mainCentralWidget.setObjectName("mainCentralWidget")

        self.MainWindow.setCentralWidget(self.mainCentralWidget)

        self.menubarFrame = QtWidgets.QFrame(self.mainCentralWidget)
        self.menubarFrame.setGeometry(QtCore.QRect(0, 0, 71, 591))
        self.menubarFrame.setStyleSheet("background-color: " + f"rgb({self.themeColAct_rb});")
        self.menubarFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.menubarFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.menubarFrame.setObjectName("menubarFrame")
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"assets/img/home_{int(bool(self.themeCol))}.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.initBt = QtWidgets.QPushButton(self.menubarFrame, clicked = lambda: self.selectMenu(menu = 'home'))
        self.initBt.setGeometry(QtCore.QRect(0, 0, 71, 61))
        self.initBt.setFocusPolicy(QtCore.Qt.NoFocus)
        self.initBt.setStyleSheet("QPushButton#initBt{border: none;" + f"background-color: rgb({self.themeHovActCol});" + "}QPushButton#initBt:hover{" + f"background-color: rgb({self.themeHovCol});" + "}")
        self.initBt.setIcon(icon)
        self.initBt.setIconSize(QtCore.QSize(32, 32))
        self.initBt.setObjectName("initBt")

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"assets/img/heart_{int(bool(self.themeCol))}.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.favoriteBt = QtWidgets.QPushButton(self.menubarFrame, clicked = lambda: self.selectMenu(menu = 'favourite'))
        self.favoriteBt.setGeometry(QtCore.QRect(0, 61, 71, 61))
        self.favoriteBt.setFocusPolicy(QtCore.Qt.NoFocus)
        self.favoriteBt.setStyleSheet("QPushButton#favoriteBt{border: none;}QPushButton#favoriteBt:hover{" + f"background-color: rgb({self.themeHovCol});" + "}")
        self.favoriteBt.setIcon(icon)
        self.favoriteBt.setIconSize(QtCore.QSize(32, 32))
        self.favoriteBt.setObjectName("favoriteBt")

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"assets/img/settings_{int(bool(self.themeCol))}.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.settingsBt = QtWidgets.QPushButton(self.menubarFrame, clicked = lambda: self.selectMenu(menu = 'settings'))
        self.settingsBt.setGeometry(QtCore.QRect(0, 520, 71, 61))
        self.settingsBt.setFocusPolicy(QtCore.Qt.NoFocus)
        self.settingsBt.setStyleSheet("QPushButton#settingsBt{border: none;}QPushButton#settingsBt:hover{" + f"background-color: rgb({self.themeHovCol});" + "}")
        self.settingsBt.setIcon(icon)
        self.settingsBt.setIconSize(QtCore.QSize(32, 32))
        self.settingsBt.setObjectName("settingsBt")
        
        self.addLinkFrame = QtWidgets.QFrame(self.mainCentralWidget)
        self.addLinkFrame.setGeometry(QtCore.QRect(71, 410, 711, 181))
        self.addLinkFrame.setStyleSheet(f"background-color: rgb({self.themeCol_rb});")
        self.addLinkFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.addLinkFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.addLinkFrame.setObjectName("addLinkFrame")
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"assets/img/plus-square_{int(bool(self.themeCol))}.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.addLinkBt = QtWidgets.QPushButton(self.addLinkFrame, clicked = lambda: self.addLink(self.userEnteredTitle.text(), self.userEnteredLink.text(), self.link2img(self.userEnteredLink.text())))
        self.addLinkBt.setGeometry(QtCore.QRect(600, 120, 93, 31))
        self.addLinkBt.setFocusPolicy(QtCore.Qt.NoFocus)
        self.addLinkBt.setStyleSheet("border: none;")
        self.addLinkBt.setIcon(icon)
        self.addLinkBt.setIconSize(QtCore.QSize(32, 32))
        self.addLinkBt.setShortcut("Ctrl+Return")
        self.addLinkBt.setObjectName("addLinkBt")
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"assets/img/delete_{int(bool(self.themeCol))}.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.deleteUserLinkBt = QtWidgets.QPushButton(self.addLinkFrame, clicked = lambda: self.deleteContAdd())
        self.deleteUserLinkBt.setGeometry(QtCore.QRect(600, 40, 91, 31))
        self.deleteUserLinkBt.setFocusPolicy(QtCore.Qt.NoFocus)
        self.deleteUserLinkBt.setStyleSheet("border: none;")
        self.deleteUserLinkBt.setIcon(icon)
        self.deleteUserLinkBt.setIconSize(QtCore.QSize(32, 32))
        self.deleteUserLinkBt.setShortcut("Ctrl+Backspace")
        self.deleteUserLinkBt.setObjectName("deleteUserLinkBt")
        
        self.userEnteredLink = QtWidgets.QLineEdit(self.addLinkFrame)
        self.userEnteredLink.setGeometry(QtCore.QRect(20, 122, 571, 31))
        self.userEnteredLink.setFont(self.font12)
        self.userEnteredLink.setStyleSheet("border:none;border-radius:3px;" + f"background-color:rgb({self.themeLineEdit});color:rgb({self.themeColLet_tb});")
        self.userEnteredLink.setClearButtonEnabled(True)
        self.userEnteredLink.setPlaceholderText("Enter the link")
        self.userEnteredLink.setObjectName("userEnteredLink")

        self.userEnteredLinkLab = QtWidgets.QLabel(self.addLinkFrame)
        self.userEnteredLinkLab.setGeometry(QtCore.QRect(20, 91, 301, 21))
        self.userEnteredLinkLab.setFont(self.font12)
        self.userEnteredLinkLab.setText("Enter the link:")
        self.userEnteredLinkLab.setStyleSheet(f'color:rgb({self.themeColLet_tb});')
        self.userEnteredLinkLab.setObjectName("userEnteredLinkLab")

        self.userEnteredTitleLab = QtWidgets.QLabel(self.addLinkFrame)
        self.userEnteredTitleLab.setGeometry(QtCore.QRect(20, 10, 301, 21))
        self.userEnteredTitleLab.setFont(self.font12)
        self.userEnteredTitleLab.setText("Enter the title:")
        self.userEnteredTitleLab.setStyleSheet(f'color:rgb({self.themeColLet_tb});')
        self.userEnteredTitleLab.setObjectName("userEnteredTitleLab")

        self.userEnteredTitle = QtWidgets.QLineEdit(self.addLinkFrame)
        self.userEnteredTitle.setGeometry(QtCore.QRect(20, 41, 571, 31))
        self.userEnteredTitle.setFont(self.font12)
        self.userEnteredTitle.setStyleSheet("background-color: rgb(255, 255, 255);border:none;border-radius:3px;" + f"background-color:rgb({self.themeLineEdit});color:rgb({self.themeColLet_tb});")
        self.userEnteredTitle.setClearButtonEnabled(True)
        self.userEnteredTitle.setPlaceholderText("Enter the title")
        self.userEnteredTitle.setObjectName("userEnteredTitle")

        self.noLinksScrollArea = QtWidgets.QScrollArea(self.mainCentralWidget)
        self.noLinksScrollArea.setGeometry(QtCore.QRect(71, 0, 701, 401))
        self.noLinksScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.noLinksScrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.noLinksScrollArea.setWidgetResizable(True)
        self.noLinksScrollArea.setStyleSheet(self.MainWinCol)
        self.noLinksScrollArea.setObjectName("noLinksScrollArea")
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 701, 401))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.configContentScrollArea = QtWidgets.QScrollArea(self.mainCentralWidget)
        self.configContentScrollArea.setGeometry(QtCore.QRect(71, 0, 701, 571))
        self.configContentScrollArea.setStyleSheet("")
        self.configContentScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.configContentScrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.configContentScrollArea.setWidgetResizable(True)
        self.configContentScrollArea.setHidden(True)
        self.configContentScrollArea.setObjectName("configContentScrollArea")
        
        self.config1ContentScrollAreaWidgetContents = QtWidgets.QWidget()
        self.config1ContentScrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 701, 571))
        self.config1ContentScrollAreaWidgetContents.setStyleSheet(self.MainWinCol)
        self.config1ContentScrollAreaWidgetContents.setObjectName("config1ContentScrollAreaWidgetContents")
        
        self.config1GridLayout = QtWidgets.QGridLayout(self.config1ContentScrollAreaWidgetContents)
        self.config1GridLayout.setObjectName("config1GridLayout")
        
        self.ConfigBtsFrame = QtWidgets.QFrame(self.config1ContentScrollAreaWidgetContents)
        self.ConfigBtsFrame.setMinimumSize(QtCore.QSize(300, 0))
        self.ConfigBtsFrame.setMaximumSize(QtCore.QSize(300, 16777215))
        self.ConfigBtsFrame.setStyleSheet(f'background-color:rgb({self.themeCol_rb});')
        self.ConfigBtsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ConfigBtsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ConfigBtsFrame.setObjectName("ConfigBtsFrame")
        
        self.configGridLayout = QtWidgets.QGridLayout(self.ConfigBtsFrame)
        self.configGridLayout.setObjectName("configGridLayout")
        
        self.btsScrollArea = QtWidgets.QScrollArea(self.ConfigBtsFrame)
        self.btsScrollArea.setMinimumSize(QtCore.QSize(240, 300))
        self.btsScrollArea.setMaximumSize(QtCore.QSize(240, 300))
        self.btsScrollArea.setStyleSheet(f'background-color:rgb({self.themeCol_rb});')
        self.btsScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.btsScrollArea.setWidgetResizable(True)
        self.btsScrollArea.setObjectName("btsScrollArea")
        
        self.config2ContentScrollAreaWidget = QtWidgets.QWidget()
        self.config2ContentScrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 240, 300))
        self.config2ContentScrollAreaWidget.setObjectName("config2ContentScrollAreaWidget")
        
        self.configVerticalLayout = QtWidgets.QVBoxLayout(self.config2ContentScrollAreaWidget)
        self.configVerticalLayout.setObjectName("configVerticalLayout")
        
        self.accountBt = QtWidgets.QPushButton(self.config2ContentScrollAreaWidget, clicked = lambda: self.confBackColorBt(1))
        self.accountBt.setMinimumSize(QtCore.QSize(0, 40))
        self.accountBt.setFocusPolicy(QtCore.Qt.NoFocus)
        self.accountBt.setFont(self.font10)
        self.accountBt.setText("My account")
        self.accountBt.setStyleSheet("QPushButton#accountBt{" + f"color:rgb({self.themeColLet_tb});" + "border:none;" + f"background-color:rgba({self.themeHovActCol}, 1);" + "border-radius: 7px;}QPushButton#accountBt:hover{" + f"background-color:rgba({self.themeHovCol}, 1)" + "}")
        self.accountBt.setObjectName("accountBt")
        
        self.configVerticalLayout.addWidget(self.accountBt)
        
        self.appearanceBt = QtWidgets.QPushButton(self.config2ContentScrollAreaWidget, clicked = lambda: self.confBackColorBt(2))
        self.appearanceBt.setMinimumSize(QtCore.QSize(0, 40))
        self.appearanceBt.setFocusPolicy(QtCore.Qt.NoFocus)
        self.appearanceBt.setFont(self.font10)
        self.appearanceBt.setText("Appearance")
        self.appearanceBt.setStyleSheet("QPushButton#appearanceBt{" + f"color:rgb({self.themeColLet_tb});" + "border:none;background-color:rgba(0,0,0,0);border-radius: 7px;}QPushButton#appearanceBt:hover{" + f"background-color:rgba({self.themeHovCol}, 1)" + "}")
        self.appearanceBt.setObjectName("appearanceBt")
        
        self.configVerticalLayout.addWidget(self.appearanceBt)
        
        self.aboutBt = QtWidgets.QPushButton(self.config2ContentScrollAreaWidget, clicked = lambda: self.confBackColorBt(3))
        self.aboutBt.setMinimumSize(QtCore.QSize(0, 40))
        self.aboutBt.setFocusPolicy(QtCore.Qt.NoFocus)
        self.aboutBt.setFont(self.font10)
        self.aboutBt.setText("About")
        self.aboutBt.setStyleSheet("QPushButton#aboutBt{" + f"color:rgb({self.themeColLet_tb});" + "border:none;background-color:rgba(0,0,0,0);border-radius: 7px;}QPushButton#aboutBt:hover{" + f"background-color:rgba({self.themeHovCol}, 1)" + "}")
        self.aboutBt.setObjectName("aboutBt")
        
        self.configVerticalLayout.addWidget(self.aboutBt)


        self.btsScrollArea.setWidget(self.config2ContentScrollAreaWidget)
        self.configGridLayout.addWidget(self.btsScrollArea, 0, 0, 1, 1)
        self.config1GridLayout.addWidget(self.ConfigBtsFrame, 0, 0, 1, 1)
        
        self.configContentScrollArea.setWidget(self.config1ContentScrollAreaWidgetContents)

        # Here we configure the account frame

        self.accountFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.accountFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.accountFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.accountFrame.setObjectName("accountFrame")

        self.usernameTitlteLab = QtWidgets.QLabel(self.accountFrame)
        self.usernameTitlteLab.setGeometry(QtCore.QRect(30, 20, 171, 40))
        self.usernameTitlteLab.setFont(self.fontCal10BW75)
        self.usernameTitlteLab.setStyleSheet("color:rgb(106, 106, 106)")
        self.usernameTitlteLab.setText("USERNAME")
        self.usernameTitlteLab.setObjectName("usernameTitlteLab")
        
        self.usernameLab = QtWidgets.QLabel(self.accountFrame)
        self.usernameLab.setGeometry(QtCore.QRect(30, 60, 191, 40))
        self.usernameLab.setFont(self.font12)
        self.usernameLab.setText("Username: " + str(self.username))
        self.usernameLab.setStyleSheet(f"color:rgb({self.themeColLet_tb});")
        self.usernameLab.setObjectName("usernameLab")
        
        self.passwordTitleLab = QtWidgets.QLabel(self.accountFrame)
        self.passwordTitleLab.setGeometry(QtCore.QRect(30, 290, 171, 40))
        self.passwordTitleLab.setFont(self.fontCal10BW75)
        self.passwordTitleLab.setStyleSheet("color:rgb(106, 106, 106)")
        self.passwordTitleLab.setText("PASSWORD")
        self.passwordTitleLab.setObjectName("passwordTitleLab")
        
        self.changePasswordBt = QtWidgets.QPushButton(self.accountFrame, clicked = lambda: self.changePassConfigLayout())
        self.changePasswordBt.setGeometry(QtCore.QRect(30, 350, 170, 40))
        self.changePasswordBt.setFont(self.fontD9BW75)
        self.changePasswordBt.setStyleSheet("QPushButton#changePasswordBt{color:#fff;border:none;background-color:rgb(88, 101, 242);border-radius:5px;}QPushButton#changePasswordBt:hover{background-color:rgb(71, 82, 196)}")
        self.changePasswordBt.setObjectName("changePasswordBt")
        
        self.changeUsernameBt = QtWidgets.QPushButton(self.accountFrame, clicked = lambda: self.changeUserConfigLayout())
        self.changeUsernameBt.setGeometry(QtCore.QRect(30, 110, 170, 40))
        self.changeUsernameBt.setFont(self.fontD9BW75)
        self.changeUsernameBt.setStyleSheet("QPushButton#changeUsernameBt{color:#fff;border:none;background-color:rgb(88, 101, 242);border-radius:5px;}QPushButton#changeUsernameBt:hover{background-color:rgb(71, 82, 196)}")
        self.changeUsernameBt.setObjectName("changeUsernameBt")
        
        self.saveUsernameBt = QtWidgets.QPushButton(self.accountFrame, clicked = lambda: self.changeCredentials(type = "user"))
        self.saveUsernameBt.setGeometry(QtCore.QRect(230, 110, 90, 40))
        self.saveUsernameBt.setFont(self.fontD9BW75)
        self.saveUsernameBt.setStyleSheet("QPushButton#saveUsernameBt{color:#fff;border:none;background-color:rgb(88, 101, 242);border-radius:5px;}QPushButton#saveUsernameBt:hover{background-color:rgb(71, 82, 196)}")
        self.saveUsernameBt.setText("Save")
        self.saveUsernameBt.setObjectName("saveUsernameBt")
        
        self.changeUsernameLineEdit = QtWidgets.QLineEdit(self.accountFrame)
        self.changeUsernameLineEdit.setGeometry(QtCore.QRect(30, 170, 290, 40))
        self.changeUsernameLineEdit.setFont(self.font10)
        self.changeUsernameLineEdit.setStyleSheet("border:none;border-radius:5px;" + f"background-color:rgb({self.themeLineEdit});color:rgb({self.themeColLet_tb});")
        self.changeUsernameLineEdit.setClearButtonEnabled(True)
        self.changeUsernameLineEdit.setPlaceholderText("Type your new username")
        self.changeUsernameLineEdit.setObjectName("changeUsernameLineEdit")

        self.changeUsernamePasswordConfirmationLineEdit = QtWidgets.QLineEdit(self.accountFrame)
        self.changeUsernamePasswordConfirmationLineEdit.setGeometry(QtCore.QRect(30, 230, 290, 40))
        self.changeUsernamePasswordConfirmationLineEdit.setFont(self.font10)
        self.changeUsernamePasswordConfirmationLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.changeUsernamePasswordConfirmationLineEdit.setStyleSheet("border:none;border-radius:5px;" + f"background-color:rgb({self.themeLineEdit});color:rgb({self.themeColLet_tb});")
        self.changeUsernamePasswordConfirmationLineEdit.setClearButtonEnabled(True)
        self.changeUsernamePasswordConfirmationLineEdit.setPlaceholderText("Type your actual password")
        self.changeUsernamePasswordConfirmationLineEdit.setObjectName("changeUsernamePasswordConfirmationLineEdit")

        self.savePasswordBt = QtWidgets.QPushButton(self.accountFrame, clicked = lambda: self.changeCredentials(type = "password"))
        self.savePasswordBt.setGeometry(QtCore.QRect(230, 350, 90, 40))
        self.savePasswordBt.setFont(self.fontD9BW75)
        self.savePasswordBt.setStyleSheet("QPushButton#savePasswordBt{color:#fff;border:none;background-color:rgb(88, 101, 242);border-radius:5px;}QPushButton#savePasswordBt:hover{background-color:rgb(71, 82, 196)}")
        self.savePasswordBt.setText("Save")
        self.savePasswordBt.setObjectName("savePasswordBt")
        
        self.changePasswordActualLineEdit = QtWidgets.QLineEdit(self.accountFrame)
        self.changePasswordActualLineEdit.setGeometry(QtCore.QRect(30, 410, 290, 40))
        self.changePasswordActualLineEdit.setFont(self.font10)
        self.changePasswordActualLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.changePasswordActualLineEdit.setStyleSheet("border:none;border-radius:5px;" + f"background-color:rgb({self.themeLineEdit});color:rgb({self.themeColLet_tb});")
        self.changePasswordActualLineEdit.setClearButtonEnabled(True)
        self.changePasswordActualLineEdit.setPlaceholderText("Type your actual password")
        self.changePasswordActualLineEdit.setObjectName("changePasswordActualLineEdit")
        
        self.changePasswordNewLineEdit = QtWidgets.QLineEdit(self.accountFrame)
        self.changePasswordNewLineEdit.setGeometry(QtCore.QRect(30, 470, 290, 40))
        self.changePasswordNewLineEdit.setFont(self.font10)
        self.changePasswordNewLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.changePasswordNewLineEdit.setStyleSheet("border:none;border-radius:5px;" + f"background-color:rgb({self.themeLineEdit});color:rgb({self.themeColLet_tb});")
        self.changePasswordNewLineEdit.setClearButtonEnabled(True)
        self.changePasswordNewLineEdit.setPlaceholderText("Type your new password")
        self.changePasswordNewLineEdit.setObjectName("changePasswordNewLineEdit")
        
        self.config1GridLayout.addWidget(self.accountFrame, 0, 2, 1, 1)

        self.changeUserConfigLayout()
        self.changePassConfigLayout()

        # Here we configure the appearance frame

        self.appearanceFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        # self.appearanceFrame.setAutoFillBackground(True)
        self.appearanceFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.appearanceFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.appearanceFrame.setHidden(True)
        self.appearanceFrame.setObjectName("appearanceFrame")

        self.themeConfigTitleLab = QtWidgets.QLabel(self.appearanceFrame)
        self.themeConfigTitleLab.setGeometry(QtCore.QRect(30, 20, 171, 40))
        self.themeConfigTitleLab.setFont(self.fontCal10BW75)
        self.themeConfigTitleLab.setText("COLOR THEME")
        self.themeConfigTitleLab.setStyleSheet("color:rgb(106, 106, 106)")
        self.themeConfigTitleLab.setObjectName("themeConfigTitleLab")
        
        self.darkThemeBoxFrame = QtWidgets.QFrame(self.appearanceFrame)
        self.darkThemeBoxFrame.setGeometry(QtCore.QRect(30, 80, 320, 40))
        self.darkThemeBoxFrame.setStyleSheet("QFrame#darkThemeBoxFrame{" + f"background-color:rgb({self.themeCol_rb});" + "}")
        self.darkThemeBoxFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.darkThemeBoxFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.darkThemeBoxFrame.setObjectName("darkThemeBoxFrame")
        
        self.darkThemeRadioButton = QtWidgets.QRadioButton(self.appearanceFrame)
        self.darkThemeRadioButton.setGeometry(QtCore.QRect(50, 90, 61, 20))
        self.darkThemeRadioButton.setStyleSheet('QRadioButton#darkThemeRadioButton{' + f"background-color:rgb({self.themeCol_rb});color:rgb({self.themeColLet_tb});" + "}")
        self.darkThemeRadioButton.setFont(self.font10)
        self.darkThemeRadioButton.setText("Dark")
        self.darkThemeRadioButton.toggled.connect(lambda: self.chTheme(1))
        self.darkThemeRadioButton.setObjectName("darkThemeRadioButton")
        
        self.lightThemeBoxFrame = QtWidgets.QFrame(self.appearanceFrame)
        self.lightThemeBoxFrame.setGeometry(QtCore.QRect(30, 140, 320, 40))
        self.lightThemeBoxFrame.setStyleSheet("QFrame#lightThemeBoxFrame{" + f"background-color:rgb({self.themeCol_rb});" + "}")
        self.lightThemeBoxFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lightThemeBoxFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lightThemeBoxFrame.setObjectName("lightThemeBoxFrame")
        
        self.lightThemeRadioButton = QtWidgets.QRadioButton(self.appearanceFrame)
        self.lightThemeRadioButton.setGeometry(QtCore.QRect(50, 150, 61, 20))
        self.lightThemeRadioButton.setStyleSheet('QRadioButton#lightThemeRadioButton{' + f"background-color:rgb({self.themeCol_rb});color:rgb({self.themeColLet_tb});" + "}")
        self.lightThemeRadioButton.setFont(self.font10)
        self.lightThemeRadioButton.setText("Light")
        self.lightThemeRadioButton.toggled.connect(lambda: self.chTheme(2))
        self.lightThemeRadioButton.setObjectName("lightThemeRadioButton")
        
        self.syncThemeBoxFrame = QtWidgets.QFrame(self.appearanceFrame)
        self.syncThemeBoxFrame.setGeometry(QtCore.QRect(30, 200, 320, 40))
        self.syncThemeBoxFrame.setStyleSheet("QFrame#syncThemeBoxFrame{" + f"background-color:rgb({self.themeCol_rb});" + "}")
        self.syncThemeBoxFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.syncThemeBoxFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.syncThemeBoxFrame.setObjectName("syncThemeBoxFrame")
        
        self.syncThemeRadioButton = QtWidgets.QRadioButton(self.appearanceFrame)
        self.syncThemeRadioButton.setGeometry(QtCore.QRect(50, 210, 166, 20))
        self.syncThemeRadioButton.setStyleSheet('QRadioButton#syncThemeRadioButton{' + f"background-color:rgb({self.themeCol_rb});color:rgb({self.themeColLet_tb});" + "}")
        self.syncThemeRadioButton.setFont(self.font10)
        self.syncThemeRadioButton.setText("Sync with computer")
        self.syncThemeRadioButton.toggled.connect(lambda: self.chTheme(3))
        self.syncThemeRadioButton.setObjectName("syncThemeRadioButton")

        self.informationThemeLab = QtWidgets.QLabel(self.appearanceFrame)
        self.informationThemeLab.setGeometry(QtCore.QRect(30, 260, 320, 80))
        self.informationThemeLab.setFont(self.font10)
        self.informationThemeLab.setText("You need to close and reopen the application to apply changes")
        self.informationThemeLab.setStyleSheet(f'color:rgb({self.themeColLet_tb});')
        self.informationThemeLab.setWordWrap(True)
        self.informationThemeLab.setObjectName("informationThemeLab")
        
        self.config1GridLayout.addWidget(self.appearanceFrame, 0, 2, 1, 1)

        exec("self." + ['lightThemeRadioButton', 'darkThemeRadioButton', 'syncThemeRadioButton'][self.themeCol] + ".setChecked(True)")

        # Here we configure the About frame

        self.aboutFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.aboutFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.aboutFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.aboutFrame.setHidden(True)
        self.aboutFrame.setObjectName("aboutFrame")

        self.aboutTitleLab = QtWidgets.QLabel(self.aboutFrame)
        self.aboutTitleLab.setGeometry(QtCore.QRect(30, 20, 171, 40))
        self.aboutTitleLab.setFont(self.fontCal10BW75)
        self.aboutTitleLab.setText("ABOUT")
        self.aboutTitleLab.setStyleSheet("color:rgb(106, 106, 106)")
        self.aboutTitleLab.setObjectName("aboutTitleLab")

        self.aboutLab = QtWidgets.QLabel(self.aboutFrame)
        self.aboutLab.setGeometry(QtCore.QRect(30, 60, 320, 160))
        self.aboutLab.setFont(self.font12)
        self.aboutLab.setWordWrap(True)
        self.aboutLab.setText("LinkApp has been a project started when I was in highschool, in eight grade. From here I hope you enjoyed it and find it useful.\n\nNew versions will be updated soon!\n\nFollow the author's github:")
        self.aboutLab.setStyleSheet(f"color:rgb({self.themeColLet_tb});")
        self.aboutLab.setObjectName("aboutLab")

        self.aboutLinkBt = QtWidgets.QPushButton(self.aboutFrame, clicked = lambda: webbrowser.open("https://github.com/alex-ortega-07/"))
        self.aboutLinkBt.setGeometry(QtCore.QRect(30, 210, 220, 20))
        self.aboutLinkBt.setFont(self.fontD9BW75)
        self.aboutLinkBt.setText("https://github.com/alex-ortega-07")
        self.aboutLinkBt.setStyleSheet("QPushButton#aboutLinkBt{border:none;background-color:none;text-decoration:underline;color:rgb(52,112,222);}")
        self.aboutLinkBt.setObjectName("aboutLinkBt")

        self.config1GridLayout.addWidget(self.aboutFrame, 0, 2, 1, 1)


        self.noLinksLab = QtWidgets.QLabel(self.noLinksScrollArea)
        self.noLinksLab.setFont(self.font14)
        self.noLinksLab.setText("<html><head/><body><p align=\"center\">There are no links</p></body></html>")
        self.noLinksLab.setStyleSheet(f'color:rgb({self.themeColLet_tb});')
        self.noLinksLab.setHidden(True)
        self.noLinksLab.setObjectName("noLinksLab")
        
        self.gridLayout2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout2.addWidget(self.noLinksLab)


        for i in self.links:
            self.reloadLinks([i])

        self.noLinksHid(self.links)
        
        self.noLinksScrollArea.setWidget(self.scrollAreaWidgetContents)

        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def changeCredentials(self, type = None):
        dirApp = os.path.join(os.getenv('HOMEDRIVE'), "\\LinkApp")
        os.chdir(dirApp)

        with open("password.txt") as f:
            passReal = f.readline()


        if type == "user":
            user = self.changeUsernameLineEdit.text()
            password = self.changeUsernamePasswordConfirmationLineEdit.text()

            passEncoded = hashlib.sha256(password.encode()).hexdigest()
            usEncoded = hashlib.sha256(user.encode()).hexdigest()

            if user == "" or password == "":
                msg = QMessageBox()
                msg.setWindowTitle("Fill the fields")
                msg.setText("Unable to change the user, you must fill the required fields")
                msg.setInformativeText("Fill the fields")
                msg.setIcon(QMessageBox.Warning)

                x = msg.exec_()

            else:
                if passEncoded == passReal:
                    with open("username.txt", "w") as f:
                        f.write(usEncoded)

                    msg = QMessageBox()
                    msg.setWindowTitle("Username changed")
                    msg.setText(f"The username has been changed to {user}")
                    msg.setInformativeText("Username changed")
                    msg.setIcon(QMessageBox.Warning)

                    x = msg.exec_()

                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Password incorrect")
                    msg.setText("The password entered is wrong")
                    msg.setInformativeText("Password incorrect")
                    msg.setIcon(QMessageBox.Warning)

                    x = msg.exec_()

        elif type == "password":
            actualPassword = self.changePasswordActualLineEdit.text()
            newPassword = self.changePasswordNewLineEdit.text()

            actualPasswordEncoded = hashlib.sha256(actualPassword.encode()).hexdigest()
            newPasswordEncoded = hashlib.sha256(newPassword.encode()).hexdigest()

            if actualPasswordEncoded == passReal:
                with open("password.txt", "w") as f:
                    f.write(newPasswordEncoded)

                msg = QMessageBox()
                msg.setWindowTitle("Password changed")
                msg.setText("The password has been changed")
                msg.setInformativeText("Password changed")
                msg.setIcon(QMessageBox.Warning)

                x = msg.exec_()

            else:
                msg = QMessageBox()
                msg.setWindowTitle("Password incorrect")
                msg.setText("The password entered is wrong")
                msg.setInformativeText("Password incorrect")
                msg.setIcon(QMessageBox.Warning)

                x = msg.exec_()


                

    def reloadLinks(self, links2put):
        '''
        Add a new link to the screen
        '''
        
        # for i in range(itTimes):
        for i in links2put:
            linkFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
            linkFrame.setMinimumSize(QtCore.QSize(650, 180))
            linkFrame.setMaximumSize(QtCore.QSize(650, 180))
            linkFrame.setStyleSheet(f"background-color: rgb({self.themeCol_rb});border-radius: 15px;")
            linkFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            linkFrame.setFrameShadow(QtWidgets.QFrame.Raised)
            linkFrame.setObjectName("linkFrame")

            gridLayout1 = QtWidgets.QGridLayout(linkFrame)
            gridLayout1.setObjectName("gridLayout1")

            linkInfoFram = QtWidgets.QFrame(linkFrame)
            linkInfoFram.setFrameShape(QtWidgets.QFrame.StyledPanel)
            linkInfoFram.setFrameShadow(QtWidgets.QFrame.Raised)
            linkInfoFram.setObjectName("frameCont_TLB")
                            
            gridLayout2 = QtWidgets.QGridLayout(linkInfoFram)
            gridLayout2.setObjectName("gridLayout2")

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(f"assets/img/external-link_{int(bool(self.themeCol))}.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

            goToLinkBt = QtWidgets.QPushButton(linkInfoFram, clicked = lambda: webbrowser.open(i[0]))
            goToLinkBt.setMinimumSize(QtCore.QSize(50, 0))
            goToLinkBt.setMaximumSize(QtCore.QSize(50, 16777215))
            goToLinkBt.setFocusPolicy(QtCore.Qt.NoFocus)
            goToLinkBt.setIcon(icon)
            goToLinkBt.setIconSize(QtCore.QSize(32, 32))
            goToLinkBt.setObjectName("goToLinkBt")
                            
            gridLayout2.addWidget(goToLinkBt, 0, 3, 1, 1)
                            
            titleLinkLab = QtWidgets.QLabel(linkInfoFram)
            titleLinkLab.setFont(self.font12)
            titleLinkLab.setText(i[1])
            titleLinkLab.setStyleSheet(f'color:rgb({self.themeColLet_tb});')
            titleLinkLab.setObjectName("titleLinkLab")

            gridLayout2.addWidget(titleLinkLab, 0, 0, 1, 3)

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(f"assets/img/trash_{int(bool(self.themeCol))}.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

            deleteLinkBt = QtWidgets.QPushButton(linkInfoFram, clicked = lambda: self.delLink(i[0]))
            deleteLinkBt.setMinimumSize(QtCore.QSize(50, 0))
            deleteLinkBt.setMaximumSize(QtCore.QSize(50, 16777215))
            deleteLinkBt.setFocusPolicy(QtCore.Qt.NoFocus)
            deleteLinkBt.setIcon(icon)
            deleteLinkBt.setIconSize(QtCore.QSize(32, 32))
            deleteLinkBt.setObjectName("deleteLinkBt")
                            
            gridLayout2.addWidget(deleteLinkBt, 1, 3, 1, 1)

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(f"assets/img/heart_{int(bool(self.themeCol))}.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            favLinkBt = QtWidgets.QPushButton(linkInfoFram, clicked = lambda: self.chLinkfav(i[0]))# self.addLink(self.userEnteredTitle.text(), self.userEnteredLink.text(), self.link2img(self.userEnteredLink.text()), fav = True, id_ = i[0]))
            favLinkBt.setMinimumSize(QtCore.QSize(50, 0))
            favLinkBt.setMaximumSize(QtCore.QSize(50, 16777215))
            favLinkBt.setFocusPolicy(QtCore.Qt.NoFocus)
            favLinkBt.setIcon(icon)
            favLinkBt.setIconSize(QtCore.QSize(28, 28))
            favLinkBt.setObjectName("favLinkBt")

            gridLayout2.addWidget(favLinkBt, 2, 3, 1, 1)

            linkLab = QtWidgets.QLabel(linkInfoFram)
            linkLab.setMaximumSize(QtCore.QSize(16777215, 50))
            linkLab.setFont(self.font12)
            linkLab.setText(i[0])
            linkLab.setWordWrap(True)
            linkLab.setStyleSheet(f'color:rgb({self.themeColLet_tb});')
            linkLab.setObjectName("linkLab")

            gridLayout2.addWidget(linkLab, 1, 1, 2, 2)

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(f"assets/img/paperclip_{int(bool(self.themeCol))}.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

            clipboard = QtWidgets.QPushButton(linkInfoFram, clicked = lambda: pyperclip.copy(i[0]))
            clipboard.setMinimumSize(QtCore.QSize(50, 0))
            clipboard.setMaximumSize(QtCore.QSize(50, 16777215))
            clipboard.setFocusPolicy(QtCore.Qt.NoFocus)
            clipboard.setIcon(icon)
            clipboard.setIconSize(QtCore.QSize(32, 32))
            clipboard.setObjectName("clipboard")

            gridLayout2.addWidget(clipboard, 1, 0, 2, 1)
            gridLayout1.addWidget(linkInfoFram, 5, 2, 1, 1)

            imgLinkLab = QtWidgets.QLabel(linkFrame)
            imgLinkLab.setMinimumSize(QtCore.QSize(160, 90))
            imgLinkLab.setMaximumSize(QtCore.QSize(160, 90))
            imgLinkLab.setPixmap(QtGui.QPixmap(i[3]))
            imgLinkLab.setScaledContents(self.setScaledImg)
            imgLinkLab.setObjectName("imgLinkLab")
                            
            gridLayout1.addWidget(imgLinkLab, 5, 1, 1, 1)
            self.gridLayout2.addWidget(linkFrame)

            self.linksObj.append([i[0], linkFrame, favLinkBt])

        self.uploadIconFav()

    def addLink(self, title, link, img):
        '''
        If fav equals False, it adds a link, otherwise, it adds the link to the favorites ones
        '''

        equalTitle = False
        for i in self.links:
            if title == i[1]:
                equalTitle = True
                break
        
        if (len(title.split()) == 0 or len(link.split()) == 0):
            msg = QMessageBox()
            msg.setWindowTitle('Fill the fields')
            msg.setText('You need to fill the fields in order to add a link')
            msg.setInformativeText('Fill the fields')
            msg.setIcon(QMessageBox.Warning)

            x = msg.exec_()
            
        elif len(link.split()) > 1 or not link[0].isalpha() or not '.' in link:
            msg = QMessageBox()
            msg.setWindowTitle('Invalid link')
            msg.setText("The written link isn't spelled correctly")
            msg.setIcon(QMessageBox.Warning)

            x = msg.exec_()

        elif "'" in link or '"' in link:
            msg = QMessageBox()
            msg.setWindowTitle('Invalid link')
            msg.setText("The link cannot contain any type of quotes")
            msg.setIcon(QMessageBox.Warning)

            x = msg.exec_()

        elif "'" in title or '"' in title:
            msg = QMessageBox()
            msg.setWindowTitle('Invalid title')
            msg.setText("The title cannot contain any type of quotes")
            msg.setIcon(QMessageBox.Warning)

            x = msg.exec_()

        elif equalTitle:
            msg = QMessageBox()
            msg.setWindowTitle('Invalid title')
            msg.setText("The written title has already been used")
            msg.setIcon(QMessageBox.Warning)

            x = msg.exec_()
            
            
        else:

            # Once the link and the title fit all the conditions, we add it
            if self.appMenu == 'favourite':
                self.t, self.l, self.i, self.li = title, link, img, self.linkId2Del
                msg = QMessageBox()
                msg.setWindowTitle('Add link')
                msg.setText('If you press "Ok", you will add this link to the favourite links')
                msg.setInformativeText('Are you sure you want to add this link to favourite?')
                msg.setIcon(QMessageBox.Question)
                msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Cancel)

                msg.buttonClicked.connect(self.msgReturnMessage)

                x = msg.exec_()

                if self.msgText == 'OK':
                    self.links.append([link, title, "True", img])
                    self.reloadLinks([[link, title, 'True', img]])

            elif self.appMenu == 'home':
                self.links.append([link, title, "False", img])
                self.reloadLinks([[link, title, 'False', img]])

            self.linkId2Del += 1
            self.noLinksHid(self.linksObj)
            self.uploadIconFav()

        self.updateLinksToFile()
            
    def updateLinksToFile(self):
        '''
        Update the links to a file
        '''

        with open('links.txt', 'w') as f:
            for i in self.links:
                f.write(str(i) + "\n")

    def getLinks(self):
        '''
        Convert the links at links.txt to a list
        '''

        links = list()

        with open('links.txt', 'r') as f:
            while True:
                link = f.readline()

                if link == '':
                    break

                links.append(json.loads(link.replace("'", '"')))

        return links

    def chLinkfav(self, link):
        '''
        Adds the link to fav if the link wasn't there, otherwise, it deletes the link from fav
        '''

        idLinksFav = self.getId(self.links, 'fav')

        for i in self.links:
            if i[0] == link:
                if i[0] in idLinksFav:
                    i[2] =  "False"

                else:
                    i[2] = "True"

        self.uploadIconFav()

        self.updateLinksToFile()
        
    def delLink(self, link):
        '''
        Delete a link
        '''
        
        if self.appMenu == 'favourite':
            msg = QMessageBox()
            msg.setWindowTitle('Delete link')
            msg.setText('If you press "Ok", you will delete this link from the favourite links and also from the home section')
            msg.setInformativeText('Are you sure you want to delete this link?')
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Cancel)

            msg.buttonClicked.connect(self.msgReturnMessage)

            x = msg.exec_()

        elif self.appMenu == 'home':
            msg = QMessageBox()
            msg.setWindowTitle('Delete link')
            msg.setText('If you press "Ok", you will delete this link')
            msg.setInformativeText('Are you sure you want to delete this link?')
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Cancel)

            msg.buttonClicked.connect(self.msgReturnMessage)

            x = msg.exec_()

        if self.msgText == 'OK':
            for i in self.linksObj:
                if i[0] == link:
                    i[1].setHidden(True)

            self.links = [i for i in self.links if i[0] != link]

            self.linksObj = [i for i in self.linksObj if i[0] != link]

            # Here we remove the icon image of the link, if it has it created before
            encodedLink = hashlib.sha224(link.encode('UTF-8')).hexdigest()

            if f'{encodedLink}.png' in os.listdir():
                os.remove(f'{encodedLink}.png')

            if self.appMenu == 'home':
                self.noLinksHid(self.getId(self.links, 'home'))

            elif self.appMenu == 'favourite':
                self.noLinksHid(self.getId(self.links, 'fav'))

        self.msgText = None

        self.updateLinksToFile()

    def deleteContAdd(self):
        self.userEnteredTitle.setText('')
        self.userEnteredLink.setText('')

    def link2img(self, link):
        '''
        Convert a link to an image, it returns the path of the photo
        '''

        self.setScaledImg = False

        if 'youtube.com' in link:
            if 'watch?v=' in link:
                linkCode = list(link)[::-1]
                id_ = []

                for i in linkCode:
                    if i == '/':
                        break

                    id_.append(i)

                idJoin = ''.join(id_[::-1]).replace('watch?v=', '')
                idJoin = idJoin.split("&")[0]

                try:
                    encodedLink = hashlib.sha224(link.encode('UTF-8')).hexdigest()
                    file = requests.get(f'https://i.ytimg.com/vi/{idJoin}/maxresdefault.jpg')

                    with open(f'{encodedLink}.png', 'wb') as f: 
                        f.write(file.content)

                    self.setScaledImg = True
                    return f'{encodedLink}.png' 

                except:
                    return 'assets/img/ytLink.png'
                    
            else:
                return 'assets/img/ytLink.png'

        else:
            return 'assets/img/globe.png'

    def hideYNLinks(self, hide):
        '''
        It hides all the links depending of the value of the variable hide
        '''
        
        for num, cont in enumerate(self.linksObj):
            cont[1].setHidden(hide)

    def selectMenu(self, menu = 'home'):
        self.hideYNLinks(hide = True)
        self.addLinkFrame.setHidden(False)
        self.configContentScrollArea.setHidden(True)
        self.favoriteBt.setStyleSheet("QPushButton#favoriteBt{border: none;}QPushButton#favoriteBt:hover{" + f"background-color: rgb({self.themeHovCol});" + "}")
        self.initBt.setStyleSheet("QPushButton#initBt{border: none;}QPushButton#initBt:hover{" + f"background-color: rgb({self.themeHovCol});" + "}")
        self.settingsBt.setStyleSheet("QPushButton#settingsBt{border: none;}QPushButton#settingsBt:hover{" + f"background-color: rgb({self.themeHovCol});" + "}")

        if menu == 'home':
            self.hideYNLinks(hide = False)
            self.initBt.setStyleSheet("QPushButton#initBt{border: none;" + f"background-color: rgb({self.themeHovActCol});" + "}QPushButton#initBt:hover{" + f"background-color: rgb({self.themeHovCol});" + "}")
            self.noLinksHid(self.linksObj)

        elif menu == 'favourite':
            self.favoriteBt.setStyleSheet("QPushButton#favoriteBt{border: none;" + f"background-color: rgb({self.themeHovActCol});" + "}QPushButton#favoriteBt:hover{" + f"background-color: rgb({self.themeHovCol});" + "}")
            self.appearFavLinks(self.links, self.linksObj)
            self.noLinksHid(self.getId(self.links, 'fav'))            
        
        elif menu == 'settings':
            self.settingsBt.setStyleSheet("QPushButton#settingsBt{border: none;" + f"background-color: rgb({self.themeHovActCol});" + "}QPushButton#settingsBt:hover{" + f"background-color: rgb({self.themeHovCol});" + "}")
            self.addLinkFrame.setHidden(True)
            self.configContentScrollArea.setHidden(False)
            self.noLinksHid([1])

        self.appMenu = menu

    def appearFavLinks(self, links, objLinks):
        '''
        Makes favorite links appear
        '''
        
        idLinksFav = {i[0] for i in links if i[2] == 'True'}

        for cont in objLinks:
            if cont[0] in idLinksFav:
                cont[1].setHidden(False)

    def msgReturnMessage(self, i):
        '''
        Sets self.msgText to the text clicked of the message box
        '''
        
        self.msgText = i.text()

    def noLinksHid(self, links):
        '''
        If the length of the list links is equal to cero, is going to appear a message telling the user there are no links
        '''
        
        if len(links) != 0:
            self.noLinksLab.setHidden(True)

        else:
            self.noLinksLab.setHidden(False)

    def uploadIconFav(self):
        '''
        It sets to the link the heart icon whether the link is favorite
        '''
        
        idLinksFav = self.getId(self.links, 'fav')

        for i in self.linksObj:
            icon = QtGui.QIcon()

            if i[0] in idLinksFav:
                icon.addPixmap(QtGui.QPixmap("assets/img/heartRed.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                i[2].setIcon(icon)
            
            else:
                icon.addPixmap(QtGui.QPixmap(f"assets/img/heart_{int(bool(self.themeCol))}.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                i[2].setIcon(icon)

                if self.appMenu == 'favourite':
                    self.selectMenu(menu = 'favourite')

    def confBackColorBt(self, bt):
        '''
        It sets the corresponding colors to the menubar of the configuration section
        '''
        
        self.accountBt.setStyleSheet("QPushButton#accountBt{" + f"color:rgb({self.themeColLet_tb});" + "border:none;background-color:rgba(0,0,0,0);border-radius: 7px;}QPushButton#accountBt:hover{" + f"background-color:rgb({self.themeHovCol})" + "}")
        self.appearanceBt.setStyleSheet("QPushButton#appearanceBt{" + f"color:rgb({self.themeColLet_tb});" + "border:none;background-color:rgba(0,0,0,0);border-radius: 7px;}QPushButton#appearanceBt:hover{" + f"background-color:rgb({self.themeHovCol})" + "}")
        self.aboutBt.setStyleSheet("QPushButton#aboutBt{" + f"color:rgb({self.themeColLet_tb});" + "border:none;background-color:rgba(0,0,0,0);border-radius: 7px;}QPushButton#aboutBt:hover{" + f"background-color:rgb({self.themeHovCol})" + "}")

        self.accountFrame.setHidden(True)
        self.appearanceFrame.setHidden(True)
        self.aboutFrame.setHidden(True)

        if bt == 1:
            self.accountBt.setStyleSheet("QPushButton#accountBt{" + f"color:rgb({self.themeColLet_tb});" + "border:none;" + f"background-color:rgba({self.themeHovActCol}, 1);" + "border-radius: 7px;}QPushButton#accountBt:hover{" + f"background-color:rgba({self.themeHovCol}, 1)" + "}")
            self.accountFrame.setHidden(False)

        elif bt == 2:
            self.appearanceBt.setStyleSheet("QPushButton#appearanceBt{" + f"color:rgb({self.themeColLet_tb});" + "border:none;" + f"background-color:rgba({self.themeHovActCol}, 1);" + "border-radius: 7px;}QPushButton#appearanceBt:hover{" + f"background-color:rgba({self.themeHovCol}, 1)" + "}")
            self.appearanceFrame.setHidden(False)

        elif bt == 3:
            self.aboutBt.setStyleSheet("QPushButton#aboutBt{" + f"color:rgb({self.themeColLet_tb});" + "border:none;" + f"background-color:rgba({self.themeHovActCol}, 1);" + "border-radius: 7px;}QPushButton#aboutBt:hover{" + f"background-color:rgba({self.themeHovCol}, 1)" + "}")
            self.aboutFrame.setHidden(False)

    def posAccount_chus(self, x):
        ''''
        Used to the change user and change password section
        '''
        
        self.passwordTitleLab.setGeometry(QtCore.QRect(30, 230 + x, 171, 40))
        self.changePasswordBt.setGeometry(QtCore.QRect(30, 280 + x, 170, 40))
        self.savePasswordBt.setGeometry(QtCore.QRect(230, 280 + x, 90, 40))
        self.changePasswordActualLineEdit.setGeometry(QtCore.QRect(30, 340 + x, 290, 40))
        self.changePasswordNewLineEdit.setGeometry(QtCore.QRect(30, 400 + x, 290, 40))

    def changeUserConfigLayout(self):
        self.saveUsernameBt.setHidden(self.changeUserState)
        self.changeUsernameLineEdit.setHidden(self.changeUserState)
        self.changeUsernamePasswordConfirmationLineEdit.setHidden(self.changeUserState)
        
        self.posAccount_chus(-50)
        self.changeUsernameBt.setText("Change username")
        if not self.changeUserState:
            self.posAccount_chus(60)
            self.changeUsernameBt.setText("Cancel")
            self.changeUsernameLineEdit.setText("")
            self.changeUsernamePasswordConfirmationLineEdit.setText("")

        self.changeUserState = not self.changeUserState

    def changePassConfigLayout(self):
        self.savePasswordBt.setHidden(self.changePasswordState)
        self.changePasswordActualLineEdit.setHidden(self.changePasswordState)
        self.changePasswordNewLineEdit.setHidden(self.changePasswordState)

        self.changePasswordBt.setText("Change password")
        if not self.changePasswordState:
            self.changePasswordBt.setText("Cancel")
            self.changePasswordActualLineEdit.setText("")
            self.changePasswordNewLineEdit.setText("")

        self.changePasswordState = not self.changePasswordState

    def computerTheme(self):
        try:
            import winreg
        except ImportError:
            return False
        
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        reg_keypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'

        try:
            reg_key = winreg.OpenKey(registry, reg_keypath)

        except FileNotFoundError:
            return False

        for i in range(1024):
            try:
                value_name, value, _ = winreg.EnumValue(reg_key, i)
                if value_name == 'AppsUseLightTheme':
                    return value == 0
                
            except OSError:
                break
        
        return False

    def chTheme(self, x):
        self.darkThemeRadioButton.setStyleSheet('QRadioButton#darkThemeRadioButton{' + f"background-color:rgb({self.themeCol_rb});color:rgb({self.themeColLet_tb});" + "}")
        self.darkThemeBoxFrame.setStyleSheet("QFrame#darkThemeBoxFrame{" + f"background-color:rgb({self.themeCol_rb});" + "}")
        self.lightThemeRadioButton.setStyleSheet('QRadioButton#lightThemeRadioButton{' + f"background-color:rgb({self.themeCol_rb});color:rgb({self.themeColLet_tb});" + "}")
        self.lightThemeBoxFrame.setStyleSheet("QFrame#lightThemeBoxFrame{" + f"background-color:rgb({self.themeCol_rb});" + "}")
        self.syncThemeRadioButton.setStyleSheet('QRadioButton#syncThemeRadioButton{' + f"background-color:rgb({self.themeCol_rb});color:rgb({self.themeColLet_tb});" + "}")
        self.syncThemeBoxFrame.setStyleSheet("QFrame#syncThemeBoxFrame{" + f"background-color:rgb({self.themeCol_rb});" + "}")

        if x == 1:
            self.darkThemeRadioButton.setStyleSheet('QRadioButton#darkThemeRadioButton{' + f"background-color:rgb({self.themeColAct_rb});color:rgb({self.themeColLet_tb});" + "}")
            self.darkThemeBoxFrame.setStyleSheet("QFrame#darkThemeBoxFrame{" + f"background-color:rgb({self.themeColAct_rb});" + "}")
            with open('theme.txt', 'w') as f:
                f.write('1')

        elif x == 2:
            self.lightThemeRadioButton.setStyleSheet('QRadioButton#lightThemeRadioButton{' + f"background-color:rgb({self.themeColAct_rb});color:rgb({self.themeColLet_tb});" + "}")
            self.lightThemeBoxFrame.setStyleSheet("QFrame#lightThemeBoxFrame{" + f"background-color:rgb({self.themeColAct_rb});" + "}")
            with open('theme.txt', 'w') as f:
                f.write('0')

        elif x == 3:
            self.syncThemeRadioButton.setStyleSheet('QRadioButton#syncThemeRadioButton{' + f"background-color:rgb({self.themeColAct_rb});color:rgb({self.themeColLet_tb});" + "}")
            self.syncThemeBoxFrame.setStyleSheet("QFrame#syncThemeBoxFrame{" + f"background-color:rgb({self.themeColAct_rb});" + "}")
            with open('theme.txt', 'w') as f:
                f.write(str(int(self.computerTheme())))

    def setThemeDark(self, dark):
        if dark:
            self.themeCol_rb = '47, 49, 54'
            self.themeColAct_rb = '32, 34, 37'
            self.themeColLet_tb = '255, 255, 255'
            self.themeHovCol = '52,55,60'
            self.themeHovActCol = '57, 60, 67'
            self.themeLineEdit = '64,68,75'
            self.themeBackQScrollBar = '46,51,56'
            self.themeQScrollBar = '32, 34, 37'
            self.themeQScrollBarBox = '88, 101, 242'
            self.MainWinCol = 'background-color:rgb(54,57,63);'

        else:
            self.themeCol_rb = '236, 236, 236'
            self.themeColAct_rb = '227, 229, 232'
            self.themeColLet_tb = '0, 0, 0'
            self.themeHovCol = '232,234,237'
            self.themeHovActCol = '212, 215, 220'
            self.themeLineEdit = '255,255,255'
            self.themeBackQScrollBar = '242,242,242'
            self.themeQScrollBar = '204,204,204'
            self.themeQScrollBarBox = '190,190,190'
            self.MainWinCol = ''

    def getId(self, links, type = 'home'):
        '''
        Returns a list containing the identifiers of the links
        '''
        
        if type.lower() == 'home':
            return [i[0] for i in links]

        elif type.lower() == 'fav':
            return [i[0] for i in links if i[2] == 'True']


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    ui.loginUI()
    MainWindow.show()
    sys.exit(app.exec_())
