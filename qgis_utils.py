# -*- coding: utf-8 -*-

class QgisUtils:

	@staticmethod
	def get_subsetstring(layer):
		return layer.subsetString()

	@staticmethod
	def set_subsetstring(layer, value):
		return layer.setSubsetString(value)

	@staticmethod
	def composer_printPageAsRaster(composer):
		return composer.printPageAsRaster(0)

	@staticmethod
	def composer_windowTitle(composer):
		return composer.composerWindow().windowTitle()

	@staticmethod
	def composer_composition(composer):
		return composer.composition()
	

	@staticmethod
	def composer_saveImage(image, destinationFile, format):
		return image.save(destinationFile, format)

	@staticmethod
	def composer_printResolution(composer):
		return composer.printResolution()	

	@staticmethod
	def composer_height(composer):
		return composer.paperHeight()

	@staticmethod
	def composer_width(composer):
		return composer.paperWidth()

	@staticmethod
	def composer_MapItems(composer):
		return composer.composerMapItems()

	@staticmethod
	def mapItem_boundingRect_width(mapItem):
		return mapItem.boundingRect().width()

	@staticmethod
	def boundingRect_height(mapItem):
		return mapItem.boundingRect().height()

	@staticmethod
	def currentMapExtent_xMinimum(myMap):
		return myMap.currentMapExtent().xMinimum()

	@staticmethod
	def currentMapExtent_yMinimum(myMap):
		return myMap.currentMapExtent().yMinimum()

	@staticmethod
	def currentMapExtent_xMaximum(myMap):
		return myMap.currentMapExtent().xMaximum()

	@staticmethod
	def currentMapExtent_yMaximum(myMap):
		return myMap.currentMapExtent().yMaximum()

	@staticmethod
	def layer_crs_authid(layer):
		return layer.crs().authid()
