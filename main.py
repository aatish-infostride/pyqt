
# pip install PyQt5

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication,QMainWindow, QVBoxLayout, QLabel,QLCDNumber, QMessageBox, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtGui
import pyautogui
import subprocess


class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)


    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        print("successfully loogged in with email :", email , "and", password)
        dash=dashboard()
        widget.addWidget(dash)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)

    def createaccfunction(self):
        email = self.email.text()

        if self.password.text()==self.confirmpass.text():
            print("account created successfully")
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)

class dashboard(QMainWindow):
    def __init__(self):
        super(dashboard,self).__init__()
        loadUi("interface.ui", self)
        # self.punchinbutton.clicked.connect(self.start_timer)


        self.idle_time = 0
        self.notification_shown = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_idle_time)
        self.timer.start(1000)  # Check idle time every second


    def check_idle_time(self):
        if sys.platform == "win32":
            self.idle_time = pyautogui.idle()
        else:
            output = subprocess.check_output(["xprintidle"])
            print(output)
            self.idle_time = int(output) / 1000.0
            

        if self.idle_time > 60 and not self.notification_shown:
            print(f"The system has been idle for {self.idle_time} seconds.")
            self.show_notification()
            self.notification_shown = True

    def show_notification(self):
        message_box = QMessageBox()
        message_box.setText("The system has been idle for more than 60 seconds.")
        message_box.exec_()
        
    


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()



