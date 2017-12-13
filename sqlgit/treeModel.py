#treeview sample from http://trevorius.com/scrapbook/uncategorized/pyqt-custom-abstractitemmodel/
from PyQt5 import QtCore, QtGui


class CustomNode(object):
    def __init__(self, in_data):
        self._data = in_data
        if type(in_data) == tuple:
            self._data = list(in_data)
        if type(in_data) in (str,unicode) or not hasattr(in_data, '__getitem__'):
            self._data = [in_data]

        self._columncount = len(self._data)
        self._children = []
        self._parent = None
        self._row = 0

    def data(self, in_column):
        if in_column >= 0 and in_column < len(self._data):
            return self._data[in_column]

    def columnCount(self):
        return self._columncount

    def childCount(self):
        return len(self._children)

    def child(self, in_row):
        if in_row >= 0 and in_row < self.childCount():
            return self._children[in_row]

    def parent(self):
        return self._parent

    def row(self):
        return self._row

    def addChild(self, in_child):
        in_child._parent = self
        in_child._row = len(self._children)
        self._children.append(in_child)
        self._columncount = max(in_child.columnCount(), self._columncount)


class CustomModel(QtCore.QAbstractItemModel):
    def __init__(self, in_nodes):
        QtCore.QAbstractItemModel.__init__(self)
        self._root = CustomNode(None)
        for node in in_nodes:
            self._root.addChild(node)

    def rowCount(self, in_index):
        if in_index.isValid():
            return in_index.internalPointer().childCount()
        return self._root.childCount()

    def addChild(self, in_node, in_parent):
        if not in_parent or not in_parent.isValid():
            parent = self._root
        else:
            parent = in_parent.internalPointer()
        parent.addChild(in_node)

    def index(self, in_row, in_column, in_parent=None):
        if not in_parent or not in_parent.isValid():
            parent = self._root
        else:
            parent = in_parent.internalPointer()
    
        if not QtCore.QAbstractItemModel.hasIndex(self, in_row, in_column, in_parent):
            return QtCore.QModelIndex()
    
        child = parent.child(in_row)
        if child:
            return QtCore.QAbstractItemModel.createIndex(self, in_row, in_column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, in_index):
        if in_index.isValid():
            p = in_index.internalPointer().parent()
            if p:
                return QtCore.QAbstractItemModel.createIndex(self, p.row(),0,p)
        return QtCore.QModelIndex()

    def columnCount(self, in_index):
        if in_index.isValid():
            return in_index.internalPointer().columnCount()
        return self._root.childCount()

    def data(self, in_index, role):
        if not in_index.isValid():
            return None
        node = in_index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return node.data(in_index.column())
        return None


class treeModel():
    def models(self):
        #level 0
        items = []
        items.append(CustomNode("ROGUE-VM\DEV"))

        #level 1
        dbObjectsNode = []
        dbObjectsNode.append(CustomNode("HuManEDGE"))

        #level 2
        tableNodes = []
        tableNodes.append(dbObjectsNode[0])

        #level 3
        listNodes = []
        listNodes.append(CustomNode("Tables"))
        
        listNodes[0].addChild(CustomNode("TB_master_employment_info"))
        #end level 3

        tableNodes[0].addChild(listNodes[0])
        #end level 2

        items[0].addChild(dbObjectsNode[0])
        #end level 1
        
        
        # items[1].addChild(CustomNode(["HuManEDGECLIENT"]))

        return CustomModel(items)

# def main():
#     items = []
#     for i in 'abc':
#         items.append( CustomNode(i) )
#         items[-1].addChild( CustomNode(['d','e','f']) )
#         items[-1].addChild( CustomNode(['g','h','i']) )
#     v = QtGui.QTreeView()
#     v.setModel( CustomModel(items) )
#     v.show()
#     return v
# v = main()
