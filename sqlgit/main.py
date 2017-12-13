import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from treeModel import treeModel
from functions import EventEmmitter


class ConnectionWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
		super(ConnectionWindow,self).__init__()

		#initialize window
		self.layout = ConnectLayout(parent=self)
		self.setWindowTitle("Open Connection")
		self.setWindowIcon(QtGui.QIcon('./openmonitor.png'))
		self.setCentralWidget(self.layout)
		self.setGeometry(10, 10, 250, 130)


class ConnectLayout(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(ConnectLayout, self).__init__()
		# create and set layout to place widgets
		grid_layout = QtWidgets.QGridLayout(self)

		#self.text_box = QtWidgets.QTextEdit(self)
		labelDatabase = QtWidgets.QLabel(self)
		labelDatabase.setText("Database")
		grid_layout.addWidget(labelDatabase, 0, 0, 1, 3)

		cmbDbase = QtWidgets.QComboBox(self)       	
		grid_layout.addWidget(cmbDbase, 1, 0, 1, 3)
		cmbDbase.addItem("Microsoft SQL Server")

		labelEdited = QtWidgets.QLabel(self)
		labelEdited.setText("Server/Instance")
		grid_layout.addWidget(labelEdited, 2, 0, 1, 3)

		cmbServers = QtWidgets.QComboBox(self)       	
		grid_layout.addWidget(cmbServers, 3, 0, 1, 3)
		cmbServers.setEditable(True)
		cmbServers.lineEdit().setMaxLength(100)

		labelAuthType = QtWidgets.QLabel(self)
		labelAuthType.setText("Authentication")
		grid_layout.addWidget(labelAuthType, 4, 0, 1, 3)

		cmbAuthType = QtWidgets.QComboBox(self)  
		cmbAuthType.addItem("Windows Authentication")
		cmbAuthType.addItem("SQL Authentication")     	
		grid_layout.addWidget(cmbAuthType, 5, 0, 1, 3)

		labelUser = QtWidgets.QLabel(self)
		labelUser.setText("UserName")
		grid_layout.addWidget(labelUser, 6, 0, 1, 3)

		txtUserName = QtWidgets.QLineEdit(self)
		grid_layout.addWidget(txtUserName, 7, 0, 1, 3)

		labelPass = QtWidgets.QLabel(self)
		labelPass.setText("Password")
		grid_layout.addWidget(labelPass, 8, 0, 1, 3)

		txtPassword = QtWidgets.QLineEdit(self)
		txtPassword.setEchoMode(QtWidgets.QLineEdit.Password)
		grid_layout.addWidget(txtPassword, 9, 0, 1, 3)


		btnOpen = QtWidgets.QPushButton('Open')
		grid_layout.addWidget(btnOpen, 10, 1)

		btnCancel = QtWidgets.QPushButton('Cancel')
		grid_layout.addWidget(btnCancel, 10, 2)




class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow,self).__init__()

		#initialize window
		self.layout = Layout(parent=self)
		self.setWindowTitle("SQLGit")
		self.setWindowIcon(QtGui.QIcon('./openmonitor.png'))
		self.setCentralWidget(self.layout)
		self.setGeometry(10, 10, 700, 600)

		# filling up a menu bar
		bar = self.menuBar()

		# File menu
		file_menu = bar.addMenu('File')

		#Open connection
		open_action = QtWidgets.QAction('Open Connection', self)
		file_menu.addAction(open_action)
		file_menu.triggered.connect(self.addConnection)

		close_action = QtWidgets.QAction('&Quit', self)
		file_menu.addAction(close_action)

		# # Edit menu
		# edit_menu = bar.addMenu('Edit')
		# # adding actions to edit menu
		# undo_action = QtWidgets.QAction('Undo', self)
		# redo_action = QtWidgets.QAction('Redo', self)
		# edit_menu.addAction(undo_action)
		# edit_menu.addAction(redo_action)

		# use `connect` method to bind signals to desired behavior
		close_action.triggered.connect(self.close)

	def addConnection(self):
		conn.show()


# class Fn():
# 	def EventEmmitter(self):
# 		print("hello")

class Layout(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(Layout, self).__init__()
		# create and set layout to place widgets

		grid_layout = QtWidgets.QGridLayout(self)

		fileParentTab = QtWidgets.QTabWidget()
		contParentTab = QtWidgets.QTabWidget()
		#contParentTab_layout = QtWidgets.QGridLayout(self)

		fileList = QtWidgets.QWidget()
		changesetListTab = QtWidgets.QWidget()
		contentTab = QtWidgets.QWidget()
		versionTab = QtWidgets.QWidget()

		#self.text_box = QtWidgets.QTextEdit(self)
		# labelEdited = QtWidgets.QLabel(self)
		# labelEdited.setText("Edited Objects")
		# grid_layout.addWidget(labelEdited, 0, 0, 1, 1)
		

		lstCommits = QtWidgets.QListWidget(self)

		# model = treeModel()
		# self.trViewObjects = QtWidgets.QTreeView(self)
		# self.trViewObjects.setModel(model.models())
		# self.trViewObjects.expandToDepth(2)

		# self.trViewObjects.doubleClicked.connect(lambda: EventEmmitter(self.trViewObjects))


		dat = {
			"ZERO-VM\DEV" : {
				"HuManEDGE" : {
					"Tables" : [],
					"Views" : [],
					"Stored Procedures" : [],
					"Functions" : [] 
				}, 
				"HuManEDGECLIENT" : {
					"Tables" : [],
					"Views" : [],
					"Stored Procedures" : [],
					"Functions" : [] 
				}
			}
		}

		trViewObjects = treeModel()
		self.objListTab = QtWidgets.QTreeWidget()
		self.objListTab.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.objListTab.customContextMenuRequested.connect(self.openMenu)

		trViewObjects.generateView(self.objListTab, dat)

		#self.objListTab.customContextMenuRequested.connect(trViewObjects.openMenu)

		#p.addChild(item) 

		# item = QtWidgets.QTreeViewItem(self.trViewObjects)
		# item.setCheckState(0, QtCore.Qt.Unchecked)

		#trViewObjects.setExpanded(0, True)
		#self.versionList = QtWidgets.QListWidget(self)
		#grid_layout.addWidget(self.versionList, 1, 2, 1, 2)

		#tab

		versionList = QtWidgets.QListWidget(self)
		lstEdited = QtWidgets.QPlainTextEdit(self)

		fileParentTab.addTab(fileList, "Objects")
		fileParentTab.addTab(changesetListTab, "Changesets")
		contParentTab.addTab(contentTab,"Details")
		contParentTab.addTab(versionTab,"Versions")

		changesetListTab.layout = QtWidgets.QGridLayout(self)
		fileList.layout = QtWidgets.QGridLayout(self)
		contentTab.layout = QtWidgets.QGridLayout(self)
		versionTab.layout = QtWidgets.QGridLayout(self)

		changesetListTab.layout.addWidget(lstCommits, 0,0,1,1)
		fileList.layout.addWidget(self.objListTab,0,0,1,1)
		contentTab.layout.addWidget(lstEdited, 0,0, 1,2)
		versionTab.layout.addWidget(versionList,0,0,1,1)

		changesetListTab.setLayout(changesetListTab.layout)
		fileList.setLayout(fileList.layout)
		contentTab.setLayout(contentTab.layout)
		versionTab.setLayout(versionTab.layout)

		# end tab

		#treeview
		#trObjList = QtWidgets.QTreeView()

		#end treeview

		grid_layout.addWidget(contParentTab, 1, 0, 1, 2)
		grid_layout.addWidget(fileParentTab, 1, 2, 1, 2) #row, column, height, width
		# self.scriptDetails = QtWidgets.QListWidget(self)
		# tab_layout.addWidget(self.scriptDetails, 0, 2, 1, 2)

		# self.detailsTab = QtWidgets.QWidget()
		# grid_layout.addTab(tab_layout, 1, 4, 1, 2)
		#en tab

		# self.save_button = QtWidgets.QPushButton('Save')
		# self.clear_button = QtWidgets.QPushButton('Clear')
		# self.open_button = QtWidgets.QPushButton('Open')
		# self.quit_button = QtWidgets.QPushButton('Quit')

		# grid_layout.addWidget(self.save_button, 2, 0)
		# grid_layout.addWidget(self.clear_button, 2, 1)
		# grid_layout.addWidget(self.open_button, 2, 2)
		# grid_layout.addWidget(self.quit_button, 2, 3)

	def openMenu(self, position):

		indexes = self.objListTab.selectedIndexes()

		if indexes == []:
			menu = QtWidgets.QMenu()
			menu.addAction(self.tr("View Object/Info"))
			menu.addAction(self.tr("Compare to latest"))
			menu.addAction(self.tr("Compare to other versions"))
			menu.addAction(self.tr("Compare to other commits"))
			menu.addAction(self.tr("Revert to previous state"))
			menu.addAction(self.tr("Include/Exclude"))

			menu.exec_(self.objListTab.viewport().mapToGlobal(position))



if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	# creating main window
	mw = MainWindow()
	mw.show()

	conn = ConnectionWindow()
	
	sys.exit(app.exec_())