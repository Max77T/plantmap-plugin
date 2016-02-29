import unittest
import os.path
from generationData import *

class TestPlantmapEngine(unittest.TestCase):
	
	genData = generationData('project1',
			'aesn_project',
			'id',
			'/home/max/mapGenerate/',
			['1','2'],
			'composerPlantMap',
			'.png')

	def test_project(self):
		self.assertEqual('project1',TestPlantmapEngine.genData.projectName)

	def test_layer(self):
		self.assertNotEqual('aesn_layer',TestPlantmapEngine.genData.layer)

	def test_taxonlist(self):
		self.assertEqual(len(['1','2']),len(TestPlantmapEngine.genData.taxonList))

	def test_extension(self):
		self.assertEqual('.png',TestPlantmapEngine.genData.extension)


if __name__=='__main__':
	unittest.main()