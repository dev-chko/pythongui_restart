import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paramiko
import requests, json

# Sample_config.json 형식을 받을수 있게 구성
response = requests.get('http://example.com/config.json')

r_data = response.text.replace('\n','').replace(' ', '')
dic_data = json.loads(r_data)

script = ''
pw = ''
ip = ''
username = ''
port = 22


class MyWindow(QMainWindow, QWidget):
    def __init__(self):
        QMainWindow.__init__(self)
 
        self.setWindowTitle('ccggww server reset')
        api = ChoiceTAB()
        self.move(800,800)
        self.resize(350,245)
        self.setCentralWidget(api)
        self.show()
 
    def btnClicked(self):
        QMessageBox.information(self, "버튼", "버튼 클릭!")

class ChoiceTAB(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        tabs = QTabWidget()
        tabs.addTab(APITAB(), 'API Sever')
        tabs.addTab(NMSTAB(), 'NMS ')
        vbox = QVBoxLayout()
        vbox.addWidget(tabs)
        self.setLayout(vbox)
        self.resize(350,245)
        self.show()
        


class APITAB(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        textLabel = QLabel(self)

        self.btn1 = QPushButton('Accept Server', self)
        self.btn1.clicked.connect(self.btn1_clicked)
        self.btn2 = QPushButton('Restart Service', self)
        self.btn2.clicked.connect(self.btn2_clicked)


        self.nb = QComboBox(self)
        for i in dic_data['servers']:
            self.nb.addItem(i['hostname'])


        self.sb = QComboBox(self)
        self.sb.addItem("-------------")
        for i in dic_data['channels']:
            self.sb.addItem(i['script'])
        
        global script
        script = self.sb.currentTextChanged.connect(self.Select_script)
        self.pw_box = QLineEdit()
        self.pw_box.textChanged[str].connect(self.onPwChanged)
        



        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(QLabel('Your Name :'), 0, 0)
        grid.addWidget(QLabel('Insert Password :'), 1, 0)
        grid.addWidget(QLabel('Select Channel :'), 2, 0)

        grid.addWidget(self.pw_box, 1,1)
        grid.addWidget(self.nb, 0,1)
        grid.addWidget(self.sb, 2,1)
        grid.addWidget(self.btn1, 3,0)
        grid.addWidget(self.btn2, 3,1)

        self.setLayout(grid)
        self.show()

    @pyqtSlot()
    def btn1_clicked(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(ip, 423, username=username, password=pw)
            stdin, stdout, stderr = client.exec_command('hostname')
            ssh_date =stdout.readlines().pop()
            QMessageBox.about(self, "message", "Server_name : "+ ssh_date+" SSH 연결성공")
            client.close()
        except Exception as e:
            QMessageBox.about(self, "message", "연결 실패 error : "+ str(e))


    @pyqtSlot()
    def btn2_clicked(self):
        buttonReplay = QMessageBox.information(self, "Restart Server", script + "를 실행하겠습니까?",  QMessageBox.No | QMessageBox.Yes)
        if buttonReplay == QMessageBox.Yes:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(ip, port , username=username, password=pw)
                stdin, stdout, stderr = client.exec_command('sh /home/restart_script/'+ script)
                ssh_data = stdout.readline()
                QMessageBox.about(self, "message", ssh_data)
                client.close()
            except Exception as e:
                QMessageBox.about(self, "message", "연결 실패 error: "+ str(e))
        elif buttonReplay == QMessageBox.No:
            QMessageBox.about(self, "message", "Canncel.")

    def onPwChanged(self, text):
        global pw
        pw = text
    
    def Select_script(self, text):
        global script
        script = text
    
class NMSTAB(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        textLabel = QLabel(self)

        self.btn3 = QPushButton('Accept Server', self)
        self.btn3.clicked.connect(self.btn3_clicked)
        self.btn4 = QPushButton('Restart Service', self)
        self.btn4.clicked.connect(self.btn4_clicked)


        self.nb = QComboBox(self)
        for i in dic_data['servers']:
            self.nb.addItem(i['hostname'])


        self.sb = QComboBox(self)
        self.sb.addItem("-------------")
        for i in dic_data['lottery']:
            self.sb.addItem(i['script'])
        
        global script
        script = self.sb.currentTextChanged.connect(self.Select_script)
        self.pw_box = QLineEdit()
        self.pw_box.textChanged[str].connect(self.onPwChanged)
        


        grid = QGridLayout()
        grid.addWidget(QLabel('Your Name :'), 0, 0)
        grid.addWidget(QLabel('Insert Password :'), 1, 0)
        grid.addWidget(QLabel('Select Channel :'), 2, 0)

        grid.addWidget(self.pw_box, 1,1)
        grid.addWidget(self.nb, 0,1)
        grid.addWidget(self.sb, 2,1)
        grid.addWidget(self.btn3, 3,0)
        grid.addWidget(self.btn4, 3,1)

        self.setLayout(grid)
        self.show()

    @pyqtSlot()
    def btn3_clicked(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(ip, port , username=username, password=pw)
            stdin, stdout, stderr = client.exec_command('hostname')
            ssh_date =stdout.readlines().pop()
            QMessageBox.about(self, "message", "Server_name : "+ ssh_date+" SSH 연결성공")
            client.close()
        except Exception as e:
            QMessageBox.about(self, "message", "연결 실패 error : "+ str(e))


    @pyqtSlot()
    def btn4_clicked(self):
        buttonReplay = QMessageBox.information(self, "Restart Server", script + "를 실행하겠습니까?",  QMessageBox.No | QMessageBox.Yes)
        if buttonReplay == QMessageBox.Yes:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(ip, port , username=username, password=pw)
                stdin, stdout, stderr = client.exec_command('ls /home/restart_script/'+ script)
                ssh_data = stdout.readline()
                QMessageBox.about(self, "message", ssh_data)
                client.close()
            except Exception as e:
                QMessageBox.about(self, "message", "연결 실패 error: "+ str(e))
        elif buttonReplay == QMessageBox.No:
            QMessageBox.about(self, "message", "Canncel.")

    def onPwChanged(self, text):
        global pw
        pw = text
    
    def Select_script(self, text):
        global script
        script = text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()

