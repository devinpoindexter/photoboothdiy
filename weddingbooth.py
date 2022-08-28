import sys, os, time
import PIL
import picamera
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt, QTimer
from threading import Thread

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

countdown_length = 3

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
  
        # this will hide the title bar
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        # set the title
        self.setWindowTitle("Wedding Booth")
        # setting  the geometry of window (x,y position, width and height)
        self.setGeometry(0, 100, 800, 480) #FLAG change to (0,0,800,480)
        
        # setup UI objects
        self.createStack()

        # show all the widgets (maximized)
        #self.showMaximized() #FLAG UNCOMMENT THIS LINE IN PROD
        self.changeScreen(0)
        self.show()


#####################################################################
### GUI & Cam Setup Functions 
#####################################################################

    def createStack(self):
        self.Stack = QStackedWidget(self)
    
        self.stack1 = HomeScreen(window=self) #Home Screen (take photo + options)
        self.stack2 = CountdownScreen(window=self) #Countdown Screen
        self.stack3 = BlankScreen(window=self) #White screen
        self.stack4 = EmailScreen(window=self) #Preview screen
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

    def setupCamera(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = self.camera.MAX_RESOLUTION
        self.camera.rotation              = 0
        self.camera.hflip                 = True
        self.camera.vflip                 = False
        self.camera.brightness            = 50
        self.camera.preview_alpha = 120
        self.camera.preview_fullscreen = True
        #self.camera.framerate             = 24
        #self.camera.sharpness             = 0
        #self.camera.contrast              = 8
        #self.camera.saturation            = 0
        #self.camera.ISO                   = 0
        #self.camera.video_stabilization   = False
        #self.camera.exposure_compensation = 0
        #self.camera.exposure_mode         = 'auto'
        #self.camera.meter_mode            = 'average'
        #self.camera.awb_mode              = 'auto'
        #self.camera.image_effect          = 'none'
        #self.camera.color_effects         = None
        #self.camera.crop                  = (0.0, 0.0, 1.0, 1.0)

#####################################################################
### Screens 
#####################################################################

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
        self.window.setupCamera()
        self.countdown_start()

        

    def countdown_start(self):
        self.countdown_label.setText(str(self.seconds))
        self.countdown_timer.start(1000) #Add half second padding to give pi time to update screen


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
        try:
            self.window.camera.capture('WBphoto.jpg')
        finally:
            self.window.camera.close()
            self.window.changeScreen(3)


class EmailScreen(QWidget):
    def __init__(self, window=None):
        super().__init__()
        self.window = window
        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(0,0,800,480)
        self.email_input.editingFinished.connect(self.processEmail)
        self.setStyleSheet("background-color: white;")

    def widgetSelected(self):
        pass

    def processEmail(self):
        email = self.email_input.text()
        print(email)

#####################################################################
### Run App
#####################################################################

# Initialize app
app = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()
# start the app

sys.exit(app.exec())