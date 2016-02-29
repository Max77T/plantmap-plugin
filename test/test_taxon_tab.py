import unittest

# This import is to enable SIP API V2
# noinspection PyUnresolvedReferences
import qgis  # pylint: disable=unused-import
import qgis.utils
import sys
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer, QgsMapLayerRegistry, QgsApplication
from PyQt4 import QtCore, QtTest
from PyQt4.QtCore import *
from PyQt4.QtGui import QDialogButtonBox, QDialog

from plantmap_engine import *
from plantmap_dialog import PlantMapDialog
from utilities import get_qgis_app, test_data_path, load_layer


QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()

class TestTaxonTab(unittest.TestCase):


	
	#Test if all the value in the combobox iterationField are really in the layer
	#Test if all the layer are present in the combobox taxonLayer

	def test_remove_board(self):
		#load shape test
		print "\n"
		print "---- debut test ----- "
		testPath = test_data_path('layer','aesn_simplifie.shp') 
		layer = load_layer(testPath)
		if not layer.isValid():
			print "-/-\- failed -/-\-"
		else:
			print "---- Layer loaded ----"
		 
		#Init a qgis instance
		registry = QgsMapLayerRegistry.instance()
		#Remove all layers
		registry.addMapLayer(layer)

		# Init the qt application to interact with each widget
		self.dialog = PlantMapDialog(IFACE)

		self.dialog.UI_taxonLayer.clear()
		self.dialog.UI_taxonLayer.addItem(layer.name(),layer)
		

		#Put a value of one field 
		self.dialog.UI_iterationField.clear()
		self.dialog.UI_iterationField.addItem("cd_ref_ref")

		iterationField = self.dialog.UI_iterationField.currentText()

		#Add one taxon to the board
		self.dialog.add_Taxon_To_Board("1234","test","OK")
		self.dialog.validate_remove_all()

		self.assertEqual(self.dialog.UI_taxonTab.rowCount(),0)


	def test_status_field(self):

		print "\n"
		print "----- debut test -----"

		testPath = test_data_path('layer','aesn_simplifie.shp') 
		layer = load_layer(testPath)
		if not layer.isValid():
			print "-/-\- failed -/-\-"
		else:
			print "---- Layer loaded ----"

		#Init a qgis instance
		registry = QgsMapLayerRegistry.instance()
		#Remove all layers
		registry.addMapLayer(layer)

		# Init the qt application to interact with each widget
		self.dialog = PlantMapDialog(IFACE)

		self.dialog.UI_taxonLayer.clear()
		self.dialog.UI_taxonLayer.addItem(layer.name(),layer)

		#Put a value of one field 
		self.dialog.UI_iterationField.clear()
		self.dialog.UI_iterationField.addItem("cd_ref_ref")

		#Put a value in the combobox of descriptionField
		self.dialog.UI_descriptionField.clear()
		self.dialog.UI_descriptionField.addItem("nom_comple")

		iterationField = self.dialog.UI_iterationField.currentText()
		descriptionField = self.dialog.UI_descriptionField.currentText()		

		descriptionFeature = self.dialog.pme.check_taxon_id("222",layer,iterationField,descriptionField)

		self.assertEqual(descriptionFeature,None)

		descriptionFeature = self.dialog.pme.check_taxon_id("88949",layer,iterationField,descriptionField)

		self.assertNotEqual(descriptionFeature,None)


	def test_description_field(self):
		print "\n"
		print "----- debut test -----"

		testPath = test_data_path('layer','aesn_simplifie.shp') 
		layer = load_layer(testPath)
		if not layer.isValid():
			print "-/-\- failed -/-\-"
		else:
			print "---- Layer loaded ----"

		#Init a qgis instance
		registry = QgsMapLayerRegistry.instance()
		#Remove all layers
		registry.addMapLayer(layer)

		# Init the qt application to interact with each widget
		self.dialog = PlantMapDialog(IFACE)

		self.dialog.UI_taxonLayer.clear()
		self.dialog.UI_taxonLayer.addItem(layer.name(),layer)

		#Put a value of one field 
		self.dialog.UI_iterationField.clear()
		self.dialog.UI_iterationField.addItem("cd_ref_ref")

		#Put a value in the combobox of descriptionField
		self.dialog.UI_descriptionField.clear()
		self.dialog.UI_descriptionField.addItem("nom_comple")

		iterationField = self.dialog.UI_iterationField.currentText()
		descriptionField = self.dialog.UI_descriptionField.currentText()		

		descriptionFeature = self.dialog.pme.check_taxon_id("88949",layer,iterationField,descriptionField)

		self.assertEqual(descriptionFeature,"Carex viridula Michx. subsp. viridula")

		self.dialog.add_Taxon_To_Board("88949",descriptionFeature,"OK")

		taxonBoard = self.dialog.UI_taxonTab
		cell = taxonBoard.item(0,1).text()
		
		self.assertEqual("Carex viridula Michx. subsp. viridula",cell)
		self.assertNotEqual("fazfageaz fage",cell)
		


	def test_add_one_taxon(self):
		#self.dialog = PlantMapDialog(IFACE)

		#load shape test
		print "\n"
		print "---- debut test ----- "
		testPath = test_data_path('layer','aesn_simplifie.shp') 
		layer = load_layer(testPath)
		if not layer.isValid():
			print "-/-\- failed -/-\-"
		else:
			print "---- Layer loaded ----"
		 
		#Init a qgis instance
		registry = QgsMapLayerRegistry.instance()
		#Remove all layers
		registry.addMapLayer(layer)

		# Init the qt application to interact with each widget
		self.dialog = PlantMapDialog(IFACE)

		self.dialog.UI_taxonLayer.clear()
		self.dialog.UI_taxonLayer.addItem(layer.name(),layer)
		

		#Put a value of one field 
		self.dialog.UI_iterationField.clear()
		self.dialog.UI_iterationField.addItem("cd_ref_ref")

		iterationField = self.dialog.UI_iterationField.currentText()

		#Get the taxon board		
		taxonBoard = self.dialog.UI_taxonTab;

		#Add one taxon to the board
		self.dialog.add_Taxon_To_Board("1234","test","OK")

		#Test the tab length with a defined value
		self.assertEqual(taxonBoard.rowCount(),1)

		#Test the tab with the list which is supposed to be fill with the method
		self.assertEqual(taxonBoard.rowCount(),len(self.dialog.taxonList))




if __name__=='__main__':
	suite = unittest.makeSuite(TestTaxonTab)
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)