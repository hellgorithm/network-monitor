def EventEmmitter(index):
	# item = trViewObjects.model().index(0,0)
	# strData = item.data(0).toPyObject()
	# print('' + str(strData))

    item = index.selectedIndexes()[0]
    print(item.data(0))