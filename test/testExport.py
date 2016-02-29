import unittest
from plantmap_plugin.export import Export
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox, QComboBox
from PyQt4.QtXml import QDomDocument
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import zipfile
import os.path

class TestExport(unittest.TestCase):

	def test_generate_export_class(self):
		path = "/home/travis/build/JJardin77580/plantMap/test/poject"
		listExt = ["PNG", "JPEG", "TIFF"]
		ex = Export(path, listExt)
		self.assertTrue(ex.path, path)
		self.assertTrue(ex.listOfExtensionImg, listExt)

	def test_list_img(self):
		path = "/home/travis/build/JJardin77580/plantMap/test/poject"
		listExt = ["PNG", "JPEG", "TIFF"]
		ex = Export(path, listExt)
		ex.fill_list_of_img()
		

	def test_construc_archive(self):
		path = "/home/travis/build/JJardin77580/plantMap/test/poject"
		listExt = ["PNG", "JPEG", "TIFF"]
		ex = Export(path, listExt)
		ex.fill_list_of_img()
		ex.fill_list_of_metadata()
		ex.intersect_list_image_metadata()
		zipFile = ex.createZip()

		with zipfile.ZipFile(zipFile, "r") as z:
			z.extractall(path+"/pythanUnZip")

		os.chdir(path+'/pythanUnZip')
		self.assertTrue(os.path.isfile((path+'/pythanUnZip/plantmapTest_28.JPEG')))
		self.assertTrue(os.path.isfile((path+'/pythanUnZip/plantmapTest_51.JPEG')))
		self.assertTrue(os.path.isfile((path+'/pythanUnZip/metadata/plantmapTest_28.JPEG.json')))
		self.assertTrue(os.path.isfile((path+'/pythanUnZip/metadata/plantmapTest_51.JPEG.json')))
		self.assertFalse(os.path.isfile((path+'/pythanUnZip/plantmapTest_14.JPEG')))

if __name__=='__main__':
	unittest.main()