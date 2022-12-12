import sys, os, time, configparser, logging
import PIL
import smtplib
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import picamera
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt, QObject, QTimer, QEventLoop
from threading import Thread

#####################################################################
### Defaults and globals
#####################################################################
os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

config = configparser.ConfigParser()
config.optionxform = str
config.read('config.ini')
email_address = str(config["DEFAULT"]["SENDER-GMAIL-ADDRESS"])
email_password = str(config["DEFAULT"]["SENDER-GMAIL-PASSWORD"])
email_subject = str(config["DEFAULT"]["EMAIL-SUBJECT"])
email_body = str(config["DEFAULT"]["EMAIL-BODY"])


now = datetime.now().strftime('%m-%d-%Y')
logging.basicConfig(filename=f'logs/{now}.log', format='%(asctime)s %(message)s', level=logging.INFO)


#####################################################################
#####################################################################
### Main Window Setup
#####################################################################
#####################################################################
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
  
        # UI customizations
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Wedding Booth")
        self.setGeometry(0, 0, 800, 480) #FLAG change to (0,0,800,480)
        self.createStack()
        QGuiApplication.inputMethod().visibleChanged.connect(self.keyboardMask) # make sure keyboard doesn't block app
        self.setStyleSheet("background-color: white;")


        self.countdown_length = 3
        self.burst_count = 1
        self.photo_paths = []

        # show all the widgets (maximized)
        #self.showMaximized() #FLAG UNCOMMENT THIS LINE IN PROD
        self.changeScreen(0)
        self.show()


#####################################################################
### GUI & Cam Setup Functions 
#####################################################################

    def createStack(self):
        self.Stack = QStackedWidget(self)
    
        self.stack0 = HomeScreen(window=self) #Home Screen (take photo + options)
        self.stack1 = CountdownScreen(window=self) #Countdown Screen
        self.stack2 = BlankScreen(window=self) #White screen
        self.stack3 = EmailScreen(window=self) #Enter Email
        self.stack4 = SettingsScreen(window=self) #Admin

        self.Stack.addWidget(self.stack0)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        self.Stack.addWidget(self.stack4)
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
    def keyboardMask(self): # without this function, the keyboard "blacks out" the top of the screen and user cannot see what they're typing
        if not QGuiApplication.inputMethod().isVisible():
            return
        for w in QGuiApplication.allWindows():
            if w.metaObject().className() == "QtVirtualKeyboard::InputView":
                keyboard = w.findChild(QObject, "keyboard")
                if keyboard is not None:
                    r = w.geometry()
                    r.moveTop(keyboard.property("y"))
                    w.setMask(QRegion(r))
                    return
#####################################################################
### Screens 
#####################################################################

class HomeScreen(QWidget):
    def __init__(self, window=None):
        super().__init__()        
        self.window = window     
        self.setStyleSheet("background-color: white;")

        self.photo_button = QPushButton("", self)
        self.photo_button.setGeometry(0,0,700,480)
        self.photo_button.setStyleSheet("background-image: url(./assets/take_photo.png); border-right: 1px solid #999999;")
        countdown_screen = lambda: self.window.changeScreen(1)
        self.photo_button.clicked.connect(countdown_screen)

        self.settings_button = QPushButton("", self)
        self.settings_button.setGeometry(700,430,100,50)
        self.settings_button.setStyleSheet("background-image: url(./assets/settings_button.png); border: none")
        settings_screen = lambda: self.window.changeScreen(4)
        self.settings_button.clicked.connect(settings_screen)

        self.burst_options = [1,3,5]
        self.burst_button = QPushButton("", self)
        self.burst_button.setGeometry(700,20,100,100)
        self.burst_button.setStyleSheet("background-image: url(./assets/burst_1.png); border: none")
        self.burst_button.clicked.connect(self.changeBurst)
    
        self.timer_options = [3,5,7]
        self.timer_button = QPushButton("", self)
        self.timer_button.setGeometry(700,150,100,100)
        self.timer_button.setStyleSheet("background-image: url(./assets/countdown_3.png); border: none") #FLAG Update
        self.timer_button.clicked.connect(self.changeTimer)

    def changeBurst(self):
        self.burst_options.append(self.burst_options.pop(0)) #Cycle current value to end of loop
        new_count = self.burst_options[0]
        self.window.burst_count = new_count # Set count to new value
        self.burst_button.setStyleSheet(f'background-image: url(./assets/burst_{new_count}.png); border: none')
        
    def changeTimer(self):
        self.timer_options.append(self.timer_options.pop(0)) #Cycle current value to end of loop
        new_length = self.timer_options[0]
        self.window.countdown_length = new_length # Set count to new value
        self.timer_button.setStyleSheet(f'background-image: url(./assets/countdown_{new_length}.png); border: none')


    def widgetSelected(self): #Called on each screen when that screen becomes active.
        pass


class CountdownScreen(QWidget):
    def __init__(self, window=None):
        super().__init__()
        self.window = window
        self.countdown_label = QLabel("", self)
        self.countdown_label.setGeometry(0,0,800,480)
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setFont(QFont('Montserrat', 100))
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.countdown_end)
        
    def widgetSelected(self):
        self.window.setupCamera()
        self.seconds = self.window.countdown_length
        self.countdown_start()

        

    def countdown_start(self):
        self.countdown_label.setText(str(self.seconds))
        self.countdown_timer.start(500) #Add half second padding to give pi time to update screen


    def countdown_end(self):
        self.countdown_timer.stop()
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
        self.blank_label = QLabel("☺", self) #creating blank screen to use as flash
        self.blank_label.setFont(QFont('Montserrat', 150))
        self.blank_label.setGeometry(0,0,800,480)
        self.blank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("background-color: white;")

    def widgetSelected(self):
        self.photo_delay = QTimer()
        self.photo_delay.timeout.connect(self.take_photo)
        self.photo_delay.start(500)


    def take_photo(self):
        self.photo_delay.stop()
        self.window.camera.start_preview()
        count = 1
        self.window.photo_paths.clear()
        try:
            while count <= self.window.burst_count:
                try:
                    
                    now = datetime.now()
                    folderpath = 'photos/' + now.strftime('%Y') + '/' + now.strftime('%h') + '/' + now.strftime('%d') +'/'
                    Path().absolute().joinpath(folderpath).mkdir(parents=True, exist_ok=True)
                    filepath = folderpath + now.strftime(f'%H-%M-%S_{count}.jpg')

                    self.window.camera.capture(filepath)
                    self.window.camera.stop_preview()
                    self.window.photo_paths.append(filepath)
                finally:
                    logging.info(f'took photo {filepath}')

                count += 1
                
                if count <= self.window.burst_count: # Delay between photos
                    loop = QEventLoop()
                    QTimer.singleShot(1000, loop.quit)
                    loop.exec_()
        except Exception as e:
            pass

        self.window.camera.close()
        self.window.changeScreen(3)

class EmailScreen(QWidget):
    def __init__(self, window=None):
        super().__init__()
        self.window = window

        self.desc_label = QLabel("Where should we send your photos?", self)
        self.desc_label.setGeometry(0,0,800,50)
        self.desc_label.setFont(QFont('Montserrat', 20))
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.email_label = QLabel("Email:", self)
        self.email_label.setGeometry(0,51,100,100)
        self.email_label.setFont(QFont('Montserrat', 25))
        self.email_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(100,51,500,100)
        self.email_input.setFont(QFont('Montserrat', 30))
        self.email_input.setFocus()

        self.loading_label = QLabel("", self)
        self.loading_label.setGeometry(0,150,800,100)
        self.loading_label.setFont(QFont('Montserrat', 15))
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.success_icon = QLabel("", self)
        self.success_icon.setGeometry(0,250,800,100)
        self.success_icon.setFont(QFont('Montserrat', 50))
        self.success_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.success_icon.setStyleSheet("color: green")

        self.send_button = QPushButton("Send", self)
        self.send_button.setGeometry(610,51,190,100)
        self.send_button.clicked.connect(self.processEmail)

        self.back_button = QPushButton("⬅ Back | Retake", self)
        self.back_button.setGeometry(0,10,130,30)
        self.back_button.clicked.connect(self.confirmBack)

        self.email_delay = QTimer()
        self.email_delay.timeout.connect(self.sendEmail)

        self.reset_timer = QTimer()
        self.reset_timer.timeout.connect(self.flowComplete)


    def widgetSelected(self):
        QGuiApplication.inputMethod().show()

    def confirmBack(self):
        reply = QMessageBox.question(self, 'Go Back', 'Are you sure you want to go back and lose your photos?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.window.changeScreen(0)


    def processEmail(self):
        self.send_button.setEnabled(False)
        self.loading_label.setText("Sending, please wait...")
        self.recipient_email = self.email_input.text()
        self.email_delay.start(500)


    def sendEmail(self):
        self.email_delay.stop()
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                msg = MIMEMultipart()
                msg['Subject']  = email_subject
                msg['From']     = email_address
                msg['To']       = self.recipient_email
                body = MIMEText(email_body)
                msg.attach(body)
                print(self.window.photo_paths)
                for image in self.window.photo_paths:
                    with open(image,'rb') as f:
                        image_data = f.read()
                        print('step 4')
                    mi = MIMEImage(image_data, name=os.path.basename(image))
                    print('step 5')
                    msg.attach(mi)
                    print('step 6')
                
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(email_address,email_password)
                smtp.sendmail(email_address, self.recipient_email, msg.as_string())
                smtp.quit()
        
        except Exception as e:
            print(e)
            print(self.recipient_email)
            self.loading_label.setText("Uh oh! We're having trouble connecting, your host will have your photos after the event.")
        
        else:
            self.loading_label.setText("Email Sent! (Please check your spam folder if you don't receive it)")
            self.success_icon.setText('✓')
        finally:
            logging.info(f'Sent photo to {self.recipient_email}')
            print('starting timer')
            self.reset_timer.start(4000)
            print('running timer')

    def flowComplete(self):
        self.reset_timer.stop()
        print('finished timer')
        self.loading_label.setText("")
        self.success_icon.setText("")
        self.window.changeScreen(0)
        self.send_button.setEnabled(True)
        self.email_input.clear()
        print('screen should have changed')

class SettingsScreen(QWidget):
    def __init__(self, window=None):
        super().__init__()
        self.window = window
       
        self.back_button = QPushButton("⬅ Back | Home", self)
        self.back_button.setGeometry(0,10,130,30)
        go_back = lambda: self.window.changeScreen(0)
        self.back_button.clicked.connect(go_back)

        self.close_button = QPushButton("Exit App", self)
        self.close_button.setGeometry(100,150,150,100)
        self.close_button.clicked.connect(self.confirmClose)

        self.min_button = QPushButton("Minimize App", self)
        self.min_button.setGeometry(300,150,150,100)
        self.min_button.clicked.connect(self.window.showMinimized)

        self.email_label = QLabel("To Change Wifi: \n Minimize app & \nclick wifi icon \n in menu ", self)
        self.email_label.setGeometry(500,150,150,100)
        #self.email_label.setFont(QFont('Montserrat', 25))
        self.email_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def widgetSelected(self): #Called on each screen when that screen becomes active.
        pass
        

    def confirmClose(self):
        reply = QMessageBox.question(self, 'Exit app?', 'Are you sure you want to exit the app?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.window.close()
#####################################################################
### Run App
#####################################################################

# Initialize app
app = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()
# start the app

sys.exit(app.exec())


### PRIORITIES ###
# make sure we can even focus the camera correctly :)
# Show photo preview before and after taking
# Instead of blank screen, show preview and animation between photos
# Make Photo Graphic on home screen flash different colors

### IDEAS ###
# Add frame to a copy of the photo


### Done ###
# Option to retake instead of sending
# Do we want to select single vs burst?
# 3, 5, or 7 second delay options?