import os
import logging
import json
import sys
import unittest
from PyQt4.QtTest import QTest
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox
from PyQt4.QtXml import QDomDocument
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from qgis.core import *
from qgis.utils import*
from threading import Thread, RLock
import time

from plantmap_dialog import PlantMapDialog
from utilities import get_qgis_app

QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()

app = QApplication(sys.argv)
projectInstance = QgsProject.instance()
LOGGER = logging.getLogger('QGIS')


class TestGUI(unittest.TestCase):
	"""
		This class will test the GUI interface
	"""
	def test_export_button_names(self):
		#Name of the button
		self.assertEqual("1","1")
		self.dialog = PlantMapDialog(IFACE)
		
		localExportButton = self.dialog.UI_exportButton
		LOGGER.debug(localExportButton.text())
		#print str("test")
		self.assertEqual(localExportButton.text(),"Exporter")
	
	def test_export_path(self):
		#No path location indicate
		self.dialog = PlantMapDialog(IFACE)
		self.dialog.UI_exportPath.setText("/home/max/.qgis2/python/plugins/plantmap_plugin/")
		localExportPath = self.dialog.UI_exportPath
		self.assertEqual(localExportPath.text(),"/home/max/.qgis2/python/plugins/plantmap_plugin/")

	# def test_export_button_functionality_2(self):
	# 	self.dialog = PlantMapDialog(IFACE)
	# 	localExportButton = self.dialog.UI_exportButton
	# 	localExportPath = self.dialog.UI_exportPath
	# 	localExportPath.setText(os.path.dirname(os.path.abspath(__file__)))
	# 	print str(os.path.dirname(os.path.abspath(__file__)))
	# 	#We have to set it at true when export will be fixed
	# 	self.assertFalse(QTest.mouseClick(localExportButton,Qt.LeftButton))




# class TestGUI(unittest.TestCase):

# 	def test_list_of_taxon(self):
# 		myBoard = self.ui.UI_taxonTab
# 		print len(myBoard)

	

if __name__=='__main__':
	unittest.main()