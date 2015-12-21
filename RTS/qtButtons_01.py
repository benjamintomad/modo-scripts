# python


import lx
import lxifc
import PySide
from PySide.QtGui import *


def exportMatGrp():
	lx.command('@W:/WG/WTD_Code/trunk/wtd/modo/resources-modo/configs/wtd_shadingTools/pyscripts/exportShading.py')

def createMatGrp():
	lx.command('@W:/WG/WTD_Code/trunk/wtd/modo/resources-modo/configs/wtd_shadingTools/pyscripts/createMatGrp.py')


# To create our custom view, we subclass from lxifc.CustomView
class qt_test01(lxifc.CustomView):

	def customview_Init(self, pane):

		if pane is None:
			return False

		custPane = lx.object.CustomPane(pane)

		if not custPane.test():
			return False

		# get the parent object
		parent = custPane.GetParent()

		# convert to PySide QWidget
		widget = lx.getQWidget(parent)

		# Check that it succeeds
		if widget is not None:

			# Here we create a new layout and add a button to it
			layout = PySide.QtGui.QVBoxLayout()
			exportGrpButton = QPushButton("Export material group")
			createGrpButton = QPushButton("Create material group")
		# Increasing the font size for the button
		# f = exportGrpButton.font()
		# f.setPointSize(30)
		# exportGrpButton.setFont(f)

		# This connects the "clicked" signal of the button to the onClicked function above
		exportGrpButton.clicked.connect(exportMatGrp)
		createGrpButton.clicked.connect(createMatGrp)

		# Adds the button to our layout and adds the layout to our parent widget
		layout.addWidget(exportGrpButton)
		layout.addWidget(createGrpButton)
		layout.setContentsMargins(2, 2, 2, 2)
		widget.setLayout(layout)
		return True

		return False

# Finally, register the new custom view server to Modo
lx.bless(qt_test01, "qt_test01")