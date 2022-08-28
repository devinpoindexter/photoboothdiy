import sys
import time
import PIL
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import * 
from PyQt6.QtCore import Qt, QTimer
from threading import Thread

countdown_length = 3

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
  
        # this will hide the title bar
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        # set the title
        self.setWindowTitle("Wedding Booth")
        # setting  the geometry of window (x,y position, width and height)
        self.setGeometry(100, 100, 800, 480)
        
        # setup UI objects
        self.createStack()

        # show all the widgets (maximized)
        #self.showMaximized() #FLAG UNCOMMENT THIS LINE IN PROD
        self.changeScreen(0)
        self.show()

    def createStack(self):
        self.Stack = QStackedWidget(self)
    
        self.stack1 = HomeScreen(window=self) #Home Screen (take photo + options)
        self.stack2 = CountdownScreen(window=self) #Countdown Screen
        self.stack3 = BlankScreen(window=self) #White screen
        self.stack4 = QWidget() #Preview screen
        self.stack5 = QWidget() #Enter email

        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        self.Stack.addWidget(self.stack4)
        self.Stack.addWidget(self.stack5)
        self.Stack.currentChanged.connect(self.refreshSelected)
        self.setCentralWidget(self.Stack)
        
    def changeScreen(self,i):
        self.Stack.setCurrentIndex(i)
    
    def refreshSelected(self):
        if self.Stack.currentWidget():
            self.Stack.currentWidget().widgetSelected()

class HomeScreen(QWidget):
    def __init__(self, window=None):
        super().__init__()        
        self.window = window     
        self.photo_button = QPushButton("", self)
        self.photo_button.setGeometry(0,0,700,480)
        #FLAG Need to figure out how to make button a gif, or put gif in background using QMovie
        self.photo_button.setStyleSheet("background-image: url(./assets/take_photo.png); border: none")
        next_screen = lambda: self.window.changeScreen(1)
        self.photo_button.clicked.connect(next_screen)
        


    def widgetSelected(self):
        pass

    def flashUI(self):
        pass

    def previewUI(self):
        pass

    def emailUI(self):
        pass



class CountdownScreen(QWidget):
    def __init__(self, window=None):
        super().__init__()
        self.window = window
        self.countdown_label = QLabel("This is the countdown", self)
        self.countdown_label.setGeometry(0,0,800,480)
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setFont(QFont('Montserrat', 100))
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.countdown_end)
        self.seconds = 3
        
    def widgetSelected(self):
        self.countdown_start()
        

    def countdown_start(self):
        self.countdown_label.setText(str(self.seconds))
        self.countdown_timer.start(1000)


    def countdown_end(self):
        self.seconds -= 1
        if self.seconds > 0:
            print(self.seconds)
            self.countdown_label.setText(str(self.seconds))
            self.countdown_timer.start(1000)
        elif self.seconds == 0:
            self.window.changeScreen(2)

class BlankScreen(QWidget):
    def __init__(self, window=None):
        super().__init__()
        self.window = window
        self.blank_label = QLabel("test", self)
        self.blank_label.setGeometry(0,0,800,480)
        self.setStyleSheet("background-color: white;")

    def widgetSelected(self):
        pass


# Initialize app
app = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()
# start the app

sys.exit(app.exec())