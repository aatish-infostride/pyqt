# pip install PyQt5
import time
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication,QMainWindow, QVBoxLayout, QLabel,QLCDNumber, QMessageBox, QWidget,QPushButton,QTableWidget,QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QTime,QDate,QDateTime
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtGui
import pyautogui
import subprocess
import requests
import http


class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login2.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)


        # Create the error_label widget
        self.error_label = QtWidgets.QLabel("", self)


    def loginfunction(self):
        self.error_label = self.findChild(QtWidgets.QLabel, "error_label")
        email = self.email.text()
        password = self.password.text()

        # API_URL = "http://10.20.1.70:4000/user/login"

        # # Send a request to the login API with the email and password
        # response = requests.post(API_URL, data={'email': email, 'password': password})
        
        dash=dashboard()
        widget.addWidget(dash)
        widget.setCurrentIndex(widget.currentIndex()+1)
        print("successfully loogged in with email :", email , "and", password)

        # if response.status_code == 200:  # If the login request was successful
        # # Redirect the user to the dashboard or main application screen
        #     dash=dashboard()
        #     widget.addWidget(dash)
        #     widget.setCurrentIndex(widget.currentIndex()+1)
        #     print("successfully loogged in with email :", email , "and", password)
        # else:  # If the login request failed
        # # Display an error message to the user
        #     self.error_label.setText("Invalid email or password")


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
        loadUi("interface1.ui", self)

        self.timer1 = QTimer(self)
        self.timer1.setInterval(1000)
        self.timer1.timeout.connect(self.update_time)
        self.time_label = self.findChild(QtWidgets.QLabel, "time_display")
        self.time_label.setText('00:00:00')
        self.start_button = self.findChild(QtWidgets.QPushButton, "start_button")
        self.stop_button = self.findChild(QtWidgets.QPushButton, "stop_button")
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        # Initialize the elapsed time to 0
        self.elapsed_time = 0

        # Get a reference to the table widget
        table_widget = self.findChild(QTableWidget, "tableWidget")
        self.punchout_clicked = False
        

        # idle time function start
        self.idle_time = 0
        self.notification_shown = False
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.check_idle_time)
        self.timer2.start(1000)  # Check idle time every second

    def start(self):
    # Start the timer

        if self.punchout_clicked == False:
            self.timer1.start()
            table_widget = self.findChild(QTableWidget, "tableWidget")
            current_date = QDate.currentDate()
            # Get the current system time
            current_time = QTime.currentTime()
            current_time.toString("hh:mm:ss")
            time_string = current_time.toString("hh:mm:ss AP")
            
            # Get the current number of rows in the table
            row_count = table_widget.rowCount()

            # Insert a new row at the end of the table
            table_widget.insertRow(row_count)
            # Insert the current date in the first row and first column of the table
            # table_widget.setItem(0, 0, QTableWidgetItem(current_date.toString()))
            # table_widget.setItem(0, 1, QTableWidgetItem(time_string))

            
            table_widget.setItem(row_count, 0, QTableWidgetItem(current_date.toString()))
            table_widget.setItem(row_count, 1, QTableWidgetItem(time_string))

        self.punchout_clicked = True



    def stop(self):
        # Stop the timer
        self.timer1.stop()
        table_widget = self.findChild(QTableWidget, "tableWidget")
        current_time = QTime.currentTime()
        current_time.toString("hh:mm:ss")
        time_string = current_time.toString("hh:mm:ss AP")
        
        time = self.time_label.text()
        
        last_row = table_widget.rowCount() - 1
        table_widget.setItem(last_row, 2, QTableWidgetItem(time_string))
        table_widget.setItem(last_row, 3, QTableWidgetItem(time))

        self.punchout_clicked = False

    def update_time(self):
        # Increment the elapsed time by 1 second
        self.elapsed_time += 1
        # Format the elapsed time as a string in the HH:MM:SS format
        # elapsed_time_str = QTime(0, 0).addSecs(self.elapsed_time).toString('HH:mm:ss')
        # # Update the time display with the formatted elapsed time
        # self.time_label.setText(elapsed_time_str)

        # Convert the elapsed time to a string and update the label
        time_string = '{:02d}:{:02d}:{:02d}'.format(
            self.elapsed_time // 3600,
            self.elapsed_time % 3600 // 60,
            self.elapsed_time % 60
        )
        self.time_label.setText(time_string)



# idle time function start
        # self.idle_time = 0
        # self.notification_shown = False
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.check_idle_time)
        # self.timer.start(1000)  # Check idle time every second

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
# system idle funtion end
        
app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
# widget.setFixedWidth(800)
# widget.setFixedHeight(600)
widget.show()
app.exec_()
