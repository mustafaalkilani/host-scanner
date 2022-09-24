import sys, nmap, os
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Host Scanner')
window.setFixedWidth(1000)
window.setFixedHeight(500)
window.setStyleSheet("background: #161219;")

grid = QGridLayout()
def fram_one():
    # label widget
    label = QLabel("Host Scanner")
    label.setStyleSheet("font-size:45px; font-weight:bold; color:white; margin-top:10px;")
    label.setAlignment(QtCore.Qt.AlignCenter)
    grid.addWidget(label, 0, 0)

    # label 2 widget
    label_two = QLabel("Enter your gateway")
    label_two.setStyleSheet("font-size:16px; color:white; margin-top:10px;")
    label_two.setAlignment(QtCore.Qt.AlignCenter)
    grid.addWidget(label_two, 1, 0)

    # label 3
    global label_three
    label_three = QLabel("")
    label_three.setStyleSheet("font-size: 16px; color: white; border-top: 1px solid white; margin:10px; height:55px")
    label_three.setAlignment(QtCore.Qt.AlignLeft)
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    grid.addWidget(scroll, 5, 0)
    scroll.setWidget(label_three)
    # input box widget
    global text_box
    text_box = QLineEdit()
    text_box.setStyleSheet('background: #161219; border: 1px solid #BC006C; border-radius: 15px; padding:10px 0; color:white; margin:0 270px;')
    grid.addWidget(text_box, 2, 0)
    # button widget
    button = QPushButton("RUN", clicked=lambda: scan())
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        "*{border: 2px solid #BC006C;" +
        "border-radius:25px;" +
        "font-size:30px;" +
        "color:white;" +
        "padding: 15px 0;" +
        "margin: 30px 300px;}" +
        "*:hover{background: #BC006C}"
                         )
    window.setLayout(grid)
    grid.addWidget(button, 3, 0)


    # btn tow
    btn_two = QPushButton('Copy', clicked=lambda : copy())
    btn_two.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    btn_two.setStyleSheet("*{border: 1px solid #BC006C;color:white; font-size:16px; padding:30px 5px;} *:hover{background: #BC006C}")
    grid.addWidget(btn_two, 5, 3)
def copy():
    # copy text
    cb = QApplication.clipboard()
    cb.clear(mode=cb.Clipboard)
    cb.setText(label_three.text(), mode=cb.Clipboard)

def scan():
    global sec_window
    sec_window = QMessageBox()

    sec_window.setWindowTitle('Scanning Progress')
    global progress
    progress = QProgressBar()
    progress.setMaximum(254)
    progress.setValue(0)
    progress.setGeometry(200, 100, 200, 30)
    progress.setAlignment(QtCore.Qt.AlignCenter)
    progress.setStyleSheet("border: 1px solid #BC006C; width: 200px; margin: 10px 40px")
    timer = QTimer()
    timer.timeout.connect(Incress_Step)

    timer.start(161)
    sec_window.setStandardButtons(QMessageBox.Cancel)
    sec_window.setStyleSheet('Background: #161219; color:white;')
    sec_window.setLayout(QVBoxLayout())
    sec_window.layout().addWidget(progress, 0, 1)
    sec_window.exec_()

    network = text_box.text() + "/24"
    nm = nmap.PortScanner()
    nm.scan(hosts=network, arguments="sn")
    available_hosts = [(host, nm[host]["status"]["state"]) for host in nm.all_hosts()]
    for host, status in available_hosts:
        label_three.setText(f"{label_three.text()}\nHost\t{host}")
    text_box.setText("")
def Incress_Step():
    progress.setValue(progress.value() + 1)
    if (progress.value() == 254):
       sec_window.close()
fram_one()
window.show()
sys.exit(app.exec_())

