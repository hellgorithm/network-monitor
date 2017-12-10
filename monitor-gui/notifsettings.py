import sys, os
from PyQt4 import QtGui, QtCore, Qt
import xml.etree.cElementTree as ET
from notification import Notification

class NotificationsSettings(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(NotificationsSettings, self).__init__(parent)
		self.setGeometry(100,100,350,450)
		self.setWindowTitle("Notification Settings")
		self.setWindowIcon(QtGui.QIcon('openmonitor.png'))
		self.setFixedSize(self.size())
		self.initLabel()
		self.initTextBox()
		self.initCheckBoxes()
		self.initButtons()
		self.emailListBox()
		self.readAuthSettings()
		#self.addSeparators()
		#self.show() #test

	def addSeparators(self):
		hzLine = QtGui.QFrame(self)
		hzLine.setFrameShape(QtGui.QFrame.HLine)
		hzLine.setFrameShadow(QtGui.QFrame.Sunken)
		self.setGeometry(10,350,100,10)

	def readAuthSettings(self):
		root = ET.parse('client-config.xml').getroot()
		#doc = ET.SubElement(root, "SMTP")

		for doc in root:
			if doc.tag == "smtp":
				for smtp in doc:
					if smtp.tag == "server":
						self.txtSMTP.setText(smtp.text)
					if smtp.tag == "port":
						self.txtSMTPort.setText(smtp.text)
					if smtp.tag == "username":
						self.txtUsername.setText(smtp.text)
					if smtp.tag == "password":
						self.txtPass.setText(smtp.text)
					if smtp.tag == "auth":
						 self.checkAuth(True if smtp.text == 'True' else False)


					if smtp.tag == "emails":
						for emails in smtp:
							item = QtGui.QListWidgetItem(str(emails.text))
							self.emailList.addItem(item)
		
	def initButtons(self):
		btnTest = QtGui.QPushButton(self)
		btnTest.setText("Test")
		btnTest.setGeometry(220,410,50,30)
		btnTest.clicked.connect(self.testNotification)

		btnSave = QtGui.QPushButton(self)
		btnSave.setText("Save")
		btnSave.setGeometry(280,410,50,30)
		btnSave.clicked.connect(self.saveNotifications)

		btnAddRecipient = QtGui.QPushButton(self)
		btnAddRecipient.setText("Add")
		btnAddRecipient.setGeometry(220,260,50,30)
		btnAddRecipient.clicked.connect(self.addRecipient)

		self.btnRemoveRecipient = QtGui.QPushButton(self)
		self.btnRemoveRecipient.setText("Remove")
		self.btnRemoveRecipient.setGeometry(270,260,60,30)
		self.btnRemoveRecipient.clicked.connect(self.removeRecipient)

	def removeRecipient(self):
		for item in self.emailList.selectedItems():
			self.emailList.takeItem(self.emailList.row(item))


	def addRecipient(self):
		item = QtGui.QListWidgetItem(str(self.txtReceipient.text()))
		self.emailList.addItem(item)
		self.txtReceipient.setText("")


	def initLabel(self):
		smtp = QtGui.QLabel(self)
		smtp.setText("SMTP Server")
		smtp.setGeometry(10,10,100,30)

		smtp = QtGui.QLabel(self)
		smtp.setText("SMTP Port")
		smtp.setGeometry(280,10,100,30)

		smtp = QtGui.QLabel(self)
		smtp.setText("Username")
		smtp.setGeometry(10,100,100,30)

		smtp = QtGui.QLabel(self)
		smtp.setText("Password")
		smtp.setGeometry(10,160,100,30)

		smtp = QtGui.QLabel(self)
		smtp.setText("Add Email Addresses")
		smtp.setGeometry(10,230,120,30)



	def initCheckBoxes(self):
		self.chkAuth = QtGui.QCheckBox(self)
		self.chkAuth.setGeometry(10,70,200,30)
		self.chkAuth.setText("Allow authentication")
		self.chkAuth.toggled.connect(lambda:self.checkAuth(self.chkAuth.isChecked()))
		self.checkAuth(False)

	def initTextBox(self):
		self.txtSMTP = QtGui.QLineEdit(self)
		self.txtSMTP.setGeometry(10,40,250,30)

		self.txtSMTPort = QtGui.QLineEdit(self)
		self.txtSMTPort.setGeometry(280,40,50,30)

		self.txtUsername = QtGui.QLineEdit(self)
		self.txtUsername.setGeometry(10,130,320,30)

		self.txtPass = QtGui.QLineEdit(self)
		self.txtPass.setGeometry(10,190,320,30)
		self.txtPass.setEchoMode(QtGui.QLineEdit.Password)


		self.txtReceipient = QtGui.QLineEdit(self)
		self.txtReceipient.setGeometry(10,260,200,30)

	def saveNotifications(self):
		root = ET.parse('client-config.xml').getroot()
		

		for smtp in root:
			if smtp.tag == "smtp":
				root.remove(smtp)

		doc = ET.SubElement(root, "smtp")

		ET.SubElement(doc, "server").text = str(self.txtSMTP.text())
		ET.SubElement(doc, "port").text = str(self.txtSMTPort.text())
		ET.SubElement(doc, "auth").text = str(self.chkAuth.isChecked())
		ET.SubElement(doc, "username").text = str(self.txtUsername.text())
		ET.SubElement(doc, "password").text = str(self.txtPass.text())

		#save emails
		emails = ET.SubElement(doc, "emails")

		for x in range(self.emailList.count()):
			ET.SubElement(emails, "email").text = str(self.emailList.item(x).text())


		tree = ET.ElementTree(root)
		tree.write("client-config.xml")

		save_message = "Settings has been saved."
		reply = QtGui.QMessageBox.question(self, 'Success',  save_message, QtGui.QMessageBox.Ok)

	def checkAuth(self, isEnabled):
		if isEnabled:
			self.txtUsername.setEnabled(True)
			self.txtPass.setEnabled(True)
			self.chkAuth.setChecked(True)
		else:
			self.txtUsername.setEnabled(False)
			self.txtPass.setEnabled(False)
			self.chkAuth.setChecked(False)

	def emailListBox(self):
		self.emailList = QtGui.QListWidget(self)
		self.emailList.setGeometry(10, 300, 320,100)
		self.emailList.itemSelectionChanged.connect(self.on_selection_changed)
		self.on_selection_changed()

	def on_selection_changed(self):
		if not self.emailList.selectedItems():
			self.btnRemoveRecipient.setEnabled(False)
		else:
			self.btnRemoveRecipient.setEnabled(True)




	def testNotification(self):
		for x in range(self.emailList.count()):
			notif = Notification()
			notif.sendEmail(str(self.txtSMTP.text()), str(self.txtSMTPort.text()),  str(self.txtUsername.text()), str(self.txtPass.text()), str(self.emailList.item(x).text()), "Test Email", "This is a test email from OpenMonitor", self.chkAuth.isChecked)
