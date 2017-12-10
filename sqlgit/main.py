import sys,os
from PyQt4 import QtGui, QtCore


class Window(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		self.setGeometry(100,100,380,400)
		self.setWindowTitle("SQLGit")
		self.setWindowIcon(QtGui.QIcon('openmonitor.png'))

		self.initLabel()

		self.show() #test



	def initLabel(self):

		newConn = QtGui.QAction("&New Connection", self)
		newConn.setStatusTip('Create New Connection')
		newConn.triggered.connect(self.openConnectionWindow)

		mainMenu = self.menuBar()
		editMenu = mainMenu.addMenu('&File')
		editMenu.addAction(newConn)

	def openConnectionWindow(self):
		print("hello")

app = QtGui.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())