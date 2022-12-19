
# pip install PyQt5

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QLabel,QLCDNumber
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtGui


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

class dashboard(QDialog):
    def __init__(self):
        super(dashboard,self).__init__()
        loadUi("dashboard.ui", self)
        # self.punchinbutton.clicked.connect(self.start_timer)
        
    

    


    


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()



