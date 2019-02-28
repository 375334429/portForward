from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject
from ui import Ui_Form
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import time
import threading


class Chat(LineReceiver):

    def __init__(self, users):
        self.users = users

    def connectionMade(self):
        if self not in self.users:
            self.users.append(self)

    def connectionLost(self, reason):
        if self in self.users:
            self.users.remove(self)

    def dataReceived(self, line):
        for name in self.users:
             if name != self:
                name.sendLine(line)

class ChatFactory(Factory):

    def __init__(self):
        self.users = []

    def buildProtocol(self, addr):
        return Chat(self.users)


class MyCalc(QWidget):
    port = 0
    zhuangtai=0
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.kaishi)

    def kaishi(self):
        self.port = self.ui.lineEdit.selectedText()
        self.zhuangtai = 1
        #if self.port > 65535 or self.port < 1024:
            #pass
            #QtWidgets.QMessageBox.question(self, '警告', '退出后测试将停止,\n你确认要退出吗？',QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            #self.QMessageBox.information(self,'提示','端口号应该大于1024且小于65535')
        self.ui.pushButton.setEnabled(0)
        self.ui.pushButton.setText('正在运行')
        self.ui.lineEdit.setEnabled(0)


def portthread():
    while 1:
        if win.zhuangtai==1:
            reactor.listenTCP(int(win.port), ChatFactory())
            reactor.run()
        time.sleep(1)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MyCalc()
    win.show()
    t = threading.Thread(target=portthread)
    t.start()
    sys.exit(app.exec_())

