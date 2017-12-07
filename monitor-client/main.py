import sys, os
from PyQt4 import QtGui, QtCore, Qt
import xml.etree.cElementTree as ET


class Connections(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(Connections, self).__init__(parent)
		self.setGeometry(100,100,380,400)
		self.setWindowTitle("Connection Settings")
		self.setWindowIcon(QtGui.QIcon('openmonitor.png'))
		#self.show()


class Window(QtGui.QMainWindow):

	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(100,100,380,400)
		self.setWindowTitle("OpenMonitor Client")
		self.setWindowIcon(QtGui.QIcon('openmonitor.png'))
		self.initButtons()
		self.initTextBox()
		self.pathListBox()
		self.createXMLConfig()
		self.initLabel()
		self.show()

		self.dialog = Connections()

	def initLabel(self):

		prefAction = QtGui.QAction("&Connection", self)
		prefAction.setShortcut("Ctrl+P")
		prefAction.setStatusTip('Edit Connection')
		prefAction.triggered.connect(self.openConnectionWindow)

		mainMenu = self.menuBar()
		editMenu = mainMenu.addMenu('&Edit')
		editMenu.addAction(prefAction)

		#editAction.triggered.connect(self.close_application)

	def openConnectionWindow(self):
		#conn = Connections()
		self.dialog.show()


	def pathListBox(self):
		self.pathList = QtGui.QListWidget(self)
		self.pathList.setGeometry(10, 65, 355,290)
		#self.pathList.itemChanged.connect(self.itemChangedState)

	def appToPathList(self, path):
		if self.noDuplicates(path):
			item = QtGui.QListWidgetItem(path)
			item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
			item.setCheckState(QtCore.Qt.Checked)
			self.pathList.addItem(item)
		else:
			dup_message = "Path already added to watch list. Please select other path."
			reply = QtGui.QMessageBox.question(self, 'Error',  dup_message, QtGui.QMessageBox.Ok)
	
	# def itemChangedState(self):
	# 	for x in range(self.pathList.count()):
	# 		print(self.pathList.item(x).text())


	def initTextBox(self):
		self.txtPath = QtGui.QLineEdit(self)
		self.txtPath.setGeometry(10,30,200,30)
		self.txtPath.textChanged.connect(self.enableDisableBtnAdd)

	def enableDisableBtnAdd(self):
		path = self.txtPath.text()

		if path == '':
			self.btnAdd.setEnabled(False)
		else:
			self.btnAdd.setEnabled(True)


	def initButtons(self):
		self.btnAdd = QtGui.QPushButton("Add", self)
		self.btnAdd.setGeometry(210,30, 80,30)
		self.btnAdd.clicked.connect(self.saveSharedFolder)
		self.btnAdd.setEnabled(False)

		btnApply = QtGui.QPushButton("Apply", self)
		btnApply.setGeometry(210,360, 80,30)
		btnApply.clicked.connect(self.saveConfigData)

		btnQuit = QtGui.QPushButton("Quit", self)
		btnQuit.setGeometry(290,360, 80, 30)
		btnQuit.clicked.connect(self.close)

		btnOpenFolder = QtGui.QPushButton("Browse", self)
		btnOpenFolder.setGeometry(290,30, 80, 30)
		btnOpenFolder.clicked.connect(self.browseFolder)
	
	def saveSharedFolder(self):
		sharedFolder = self.txtPath.text();
		self.appToPathList(sharedFolder)
		self.txtPath.setText('')

	def noDuplicates(self, path):
		for x in range(self.pathList.count()):
			if self.pathList.item(x).text() == path:
				return False

		return True

	def browseFolder(self):
		folder = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
		self.txtPath.setText(folder)

	def createXMLConfig(self):

		if os.path.exists("client-config.xml"):
			print("Config exists")
			self.readConfigurations()
		else:
			self.saveConfigurations()

	def saveConfigData(self):
		self.saveConfigurations()
		success_message = "Configuration has been successfully applied."
		reply = QtGui.QMessageBox.question(self, 'Success',  success_message, QtGui.QMessageBox.Ok)


	def saveConfigurations(self):
		root = ET.Element("config")
		doc = ET.SubElement(root, "paths")

		for x in range(self.pathList.count()):
			checked = self.pathList.item(x).checkState()
			ET.SubElement(doc, "path", status=str(checked), name=str('path')).text = str(self.pathList.item(x).text())

		tree = ET.ElementTree(root)
		tree.write("client-config.xml")

	def readConfigurations(self):
		root = ET.parse('client-config.xml').getroot()

		for paths in root:
			if paths.tag == "paths":
				for path in paths:
					item = QtGui.QListWidgetItem(path.text)
					item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
					item.setCheckState(QtCore.Qt.Checked if path.get("status") == "2" else QtCore.Qt.Unchecked)
					self.pathList.addItem(item)


	def closeEvent(self, event):

		quit_msg = "Are you sure you want to exit the program? All unsaved configurations will be lost."
		reply = QtGui.QMessageBox.question(self, 'Message', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()




app = QtGui.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())