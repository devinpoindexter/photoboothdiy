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

        self.setCentralWidget(stackedExample())
        self.show()

class stackedExample(QWidget):

    def __init__(self):
        super(stackedExample, self).__init__()
        self.leftlist = QListWidget ()
        self.leftlist.insertItem (0, 'Contact' )
        self.leftlist.insertItem (1, 'Personal' )
        self.leftlist.insertItem (2, 'Educational' )
            
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = homeStack()
            
        self.stack1UI()
        self.stack2UI()

            
        self.Stack = QStackedWidget (self)
        self.Stack.addWidget (self.stack1)
        self.Stack.addWidget (self.stack2)
        self.Stack.addWidget (self.stack3)
            
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.leftlist.currentRowChanged.connect(self.display)
        self.setGeometry(300, 50, 10,10)
        self.setWindowTitle('StackedWidget demo')
        self.show()
            
    def stack1UI(self):
        layout = QFormLayout()
        layout.addRow("Name",QLineEdit())
        layout.addRow("Address",QLineEdit())
        #self.setTabText(0,"Contact Details")
        self.stack1.setLayout(layout)
            
    def stack2UI(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("Male"))
        sex.addWidget(QRadioButton("Female"))
        layout.addRow(QLabel("Sex"),sex)
        layout.addRow("Date of Birth",QLineEdit())
            
        self.stack2.setLayout(layout)
            
    def stack3UI(self):
        layout = QHBoxLayout(self.stack3)
        photo_button = QPushButton("Text", self)
        photo_button.setGeometry(0,0,700,480)
        #photo_button.setStyleSheet("background-image: url(./assets/take_photo.png); border: none")
        layout.addWidget(photo_button)
        self.stack3.setLayout(layout)
            
    def display(self,i):
        self.Stack.setCurrentIndex(i)

class homeStack(QWidget):
    def __init__(self):
        super().__init__()
        self.photo_button = QPushButton("", self)
        self.photo_button.setGeometry(0,0,700,480)
        #FLAG Need to figure out how to make button a gif, or put gif in background using QMovie
        self.photo_button.setStyleSheet("background-image: url(./assets/take_photo.png); border: none")

# Initialize app
app = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()
# start the app

sys.exit(app.exec())