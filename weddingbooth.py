import sys
import time
import PIL
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt, QTimer

countdown_length = 3

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
  
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        # set the title
        self.setWindowTitle("Wedding Booth")
        # setting  the geometry of window (x,y position, width and height)
        self.setGeometry(100, 100, 800, 480)
        # setup UI objects
        self.UIComponents()
        # show all the widgets (maximized)
        #self.showMaximized() #FLAG UNCOMMENT THIS LINE IN PROD
        self.show()
  
    def UIComponents(self):
        self.photo_button = QPushButton("", self)
        self.photo_button.setGeometry(0,0,600,480)
        self.photo_button.clicked.connect(self.photo_sequence)
        # Need to figure out how to make button a gif, or put gif in background using QMovie
        self.photo_button.setStyleSheet("background-image: url(./assets/take_photo.png); border: none")

    def countdown(self, seconds=3):
        self.countdown_label = QLabel(str(seconds))
        while seconds > 0:
            print(seconds) #FLAG remove this line in PROD
            self.countdown_label.setText(str(seconds))
            time.sleep(1)
            seconds -= 1





    def photo_sequence(self):
        print("sequence started")
        self.countdown(countdown_length)
    




# Initialize app
app = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()
# start the app

sys.exit(app.exec())