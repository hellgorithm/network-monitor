from PyQt5 import QtCore, QtWidgets


class treeModel():
    def __init__(self):
        print("Setting up models")

    def generateView(self, tw, dat):

        #tests data
        databases = "HuManEDGE|HuManEDGECLIENT".split("|")
        ddl = "Tables|Views|Stored Procedures|Functions".split("|")
        dbo = "hello|world".split("|")

        server = QtWidgets.QTreeWidgetItem(tw)
        server.setText(0, "ZERO-VM\DEV")
        server.setExpanded(True)

        for db in databases:
            dbObj = QtWidgets.QTreeWidgetItem(server)
            dbObj.setText(0, db)
            dbObj.setExpanded(True)

            for schemaObj in ddl:
                schema = QtWidgets.QTreeWidgetItem(dbObj)
                schema.setText(0, schemaObj)
                schema.setExpanded(True)

                for editables in dbo:
                    edit = QtWidgets.QTreeWidgetItem(schema)
                    edit.setText(0, editables)
                    edit.setExpanded(True)
                    edit.setCheckState(0,QtCore.Qt.Unchecked)
                    edit.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

    def new_cluster(self):
        print "New Cluster"

    def rename_cluster(self):
        print "Rename cluster"

    def delete_cluster(self):
        print "Delete cluster"

    # def openMenu(self, parent=None):
    #     self.popup_menu = QtWidgets.QMenu(parent)
    #     self.popup_menu.addAction("New", self.new_cluster)
    #     self.popup_menu.addAction("Rename", self.rename_cluster)
    #     self.popup_menu.addSeparator()
    #     self.popup_menu.addAction("Delete", self.delete_cluster)
    #     self.popup_menu.exec_(self.treeView.viewport().mapToGlobal(position))
    def openMenu(self, position):
        print("hello")
        menu = QMenu()
        menu.addAction(self.tr("Edit person"))
        menu.addAction(self.tr("Edit object/container"))
        menu.addAction(self.tr("Edit object"))
        
        menu.exec_(self.treeView.viewport().mapToGlobal(position))

        
        # if isinstance(dat,dict):
        #     for k,v in dat.iteritems():
        #         item = QtWidgets.QTreeWidgetItem(tw)
        #         item.setText(0, k)
        #         item.setCheckState(0,QtCore.Qt.Unchecked)
        #         item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        #         item.setExpanded(True)
        #         self.trViewObjects.doubleClicked.connect(lambda: EventEmmitter(self.trViewObjects))
        #         self.generateView(item, v)
        #         #p.addChild(item)        
        # else:
        #     for txt in dat:
        #         item = QtWidgets.QTreeWidgetItem(tw)
        #         item.setText(0, txt)
        #         item.setCheckState(0,QtCore.Qt.Unchecked)
        #         item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        #         item.setExpanded(True)
