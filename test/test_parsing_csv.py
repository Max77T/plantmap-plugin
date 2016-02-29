import unittest

# This import is to enable SIP API V2
# noinspection PyUnresolvedReferences
import qgis  # pylint: disable=unused-import
import qgis.utils
import sys
import collections
import csv
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer, QgsMapLayerRegistry, QgsApplication
from PyQt4 import QtCore, QtTest
from PyQt4.QtCore import *
from PyQt4.QtGui import QDialogButtonBox, QDialog

from plantmap_engine import *
from plantmap_dialog import PlantMapDialog
from utilities import get_qgis_app, test_data_path, load_layer


QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()

class TestParsingCSV(unittest.TestCase):

	def test_parsing_csv_file(self):
		# Init the qt application to interact with each widget
		self.dialog = PlantMapDialog(IFACE)
		testPath = test_data_path('test.csv') 
		countRow = 0
		taxonsLocal=[]
		with open(testPath, 'r') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			for row in spamreader:
				countRow+=1
				taxonsLocal.append(row[0])

		taxons = self.dialog.parsing_csv_file(testPath)
		self.assertEqual(len(taxons),countRow)

		compare = lambda x,y:collections.Counter(x) == collections.Counter(y)
		
		self.assertTrue(compare)


if __name__=='__main__':
	suite = unittest.makeSuite(TestParsingCSV)
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)