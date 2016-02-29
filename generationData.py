import os

class generationData(object):
	"""
		This class represent the metadata of a generation
	"""
	#TODO : Add the name of the map
	projectName = '' # TODO : xml object
	layer = '' # layerObject
	mapName = '' # name of the maps
	iterationField = '' # fields combobox
	storagePath = '' # Path location of map, lineedit
	taxonList = None # taxon list
	composer = '' # composer object, combobox
	extension = '' # image type (png, jpeg or tiff), combobox
	whereEditable = '' #The filter added by the user
	

	def __init__(self, projectName, mapName, layer, iterationField,  storagePath, taxonList, composer, extension, whereEditable):
		self.projectName = projectName
		self.layer = layer
		self.mapName = mapName
		self.iterationField = iterationField
		self.storagePath = storagePath
		self.taxonList = taxonList
		self.composer = composer
		self.extension = extension
		self.whereEditable = whereEditable

	