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
import pyautogui


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

        self.time_label = self.findChild(QtWidgets.QLabel, "time_display")
        self.time_label.setText('00:00:00')
        self.start_button = self.findChild(QtWidgets.QPushButton, "start_button")
        self.stop_button = self.findChild(QtWidgets.QPushButton, "stop_button")
        self.start_button.clicked.connect(self.start_function)
        self.stop_button.clicked.connect(self.stop_function)
        # Initialize the elapsed time to 0
        self.elapsed_time = 0

        # Get a reference to the table widget
        table_widget = self.findChild(QTableWidget, "tableWidget")
        holiday_table = self.findChild(QTableWidget, "holiday_table")
        holiday_table.setItem(0, 0, QTableWidgetItem("New Year Day"))
        holiday_table.setItem(0, 1, QTableWidgetItem("07/04/2022"))
        holiday_table.setItem(0, 2, QTableWidgetItem("Monday"))
        holiday_table.setItem(1, 0, QTableWidgetItem("Memorial Day"))
        holiday_table.setItem(1, 1, QTableWidgetItem("05/30/2022"))
        holiday_table.setItem(1, 2, QTableWidgetItem("Monday"))
        holiday_table.setItem(2, 0, QTableWidgetItem("Independence Day "))
        holiday_table.setItem(2, 1, QTableWidgetItem("07/04/2022"))
        holiday_table.setItem(2, 2, QTableWidgetItem("Monday"))
        holiday_table.setItem(3, 0, QTableWidgetItem("Labor Day"))
        holiday_table.setItem(3, 1, QTableWidgetItem("09/05/2022"))
        holiday_table.setItem(3, 2, QTableWidgetItem("Monday"))
        holiday_table.setItem(4, 0, QTableWidgetItem("Deepavali"))
        holiday_table.setItem(4, 1, QTableWidgetItem("10/24/2022"))
        holiday_table.setItem(4, 2, QTableWidgetItem("Monday"))
        holiday_table.setItem(5, 0, QTableWidgetItem("Extended Diwali Holiday"))
        holiday_table.setItem(5, 1, QTableWidgetItem("10/25/2022"))
        holiday_table.setItem(5, 2, QTableWidgetItem("Tuesday"))
        holiday_table.setItem(6, 0, QTableWidgetItem("Pre-Thanks giving Day"))
        holiday_table.setItem(6, 1, QTableWidgetItem("11/23/2022"))
        holiday_table.setItem(6, 2, QTableWidgetItem("Wednesday"))
        holiday_table.setItem(7, 0, QTableWidgetItem("Thanksgiving Day "))
        holiday_table.setItem(7, 1, QTableWidgetItem("11/24/2022"))
        holiday_table.setItem(7, 2, QTableWidgetItem("Thursday"))
        holiday_table.setItem(8, 0, QTableWidgetItem("Day after Thanksgiving Day"))
        holiday_table.setItem(8, 1, QTableWidgetItem("11/25/2022"))
        holiday_table.setItem(8, 2, QTableWidgetItem("Friday"))
        self.punchout_clicked = False


    def start_function(self):
    # Start the timer
        if self.punchout_clicked == False :
            table_widget = self.findChild(QTableWidget, "tableWidget")
            current_date = QDate.currentDate()
            self.timer1 = QTimer(self)
            self.timer1.setInterval(1000)
            self.timer1.timeout.connect(self.update_time)
            self.timer1.start()

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.check_idle_time)
            self.timer.start(1000)  # 1000 milliseconds = 1 second
            
            # Get the current system time
            current_time = QTime.currentTime()
            current_time.toString("hh:mm:ss")
            time_string = current_time.toString("hh:mm:ss AP")
            
            # Get the current number of rows in the table
            row_count = table_widget.rowCount()
            print(row_count)

            # Insert a new row at the end of the table
            table_widget.insertRow(row_count)

            table_widget.setItem(row_count, 0, QTableWidgetItem(current_date.toString()))
            
            table_widget.setItem(row_count, 1, QTableWidgetItem(time_string))

            

        self.punchout_clicked = True



    def stop_function(self):
        # Stop the timer
        self.timer1.stop()
        self.timer.stop()
        table_widget = self.findChild(QTableWidget, "tableWidget")
        current_time = QTime.currentTime()
        current_time.toString("hh:mm:ss")
        time_string = current_time.toString("hh:mm:ss AP")
        
        time = self.time_label.text()
        
        last_row = table_widget.rowCount() - 1
        table_widget.setItem(last_row, 2, QTableWidgetItem(time_string))
        table_widget.setItem(last_row, 3, QTableWidgetItem(time))
        self.time_label.setText('00:00:00')
        self.elapsed_time = 0
        self.punchout_clicked = False

    def update_time(self):
        # Increment the elapsed time by 1 second
        self.elapsed_time += 1

        # Convert the elapsed time to a string and update the label
        time_string = '{:02d}:{:02d}:{:02d}'.format(
            self.elapsed_time // 3600,
            self.elapsed_time % 3600 // 60,
            self.elapsed_time % 60
        )
        self.time_label.setText(time_string)


    def check_idle_time(self):
        # Run the xprintidle command and get the output
        output = subprocess.run(["xprintidle"], stdout=subprocess.PIPE).stdout.decode().strip()

        # Parse the output as an integer
        idle_time = int(output)

        # Check if the idle time is 5 seconds or more
        if idle_time >= 5000:  # 5000 milliseconds = 5 seconds
            # Show a notification using a message box
            QMessageBox.warning(self, "Idle Time", "You have been idle for 5 seconds!")
    


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
# widget.setFixedWidth(800)
# widget.setFixedHeight(600)
widget.show()
app.exec_()
