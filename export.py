# -*- coding: utf-8 -*-
import time
import glob, os
import zipfile
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox, QComboBox
from PyQt4.QtXml import QDomDocument
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from logger import *

class Export:
	"""
	This class create the zip file with the images and metadata in a folder
	The folder is pass in argument of __init__
	Extension of images must be in listOfExtensionImg 
	If a images dosn't have a metadata, images deosn't in archive
	If a metadata deosn't have a images, metadata deosn't in archive
	The archive is create in the folder
	"""

	def __init__(self, path, listOfExtensionImg):
		self.path = None
		self.listOfExtensionImg = []
		self.listOfImg = []
		self.listOfMetadata = []
		self.listOfImgToArchive = []
		self.path = path
		self.listOfExtensionImg = listOfExtensionImg
		self.nameZipFile = os.path.basename(os.path.normpath(path))
	
	def process(self):
		"""
			Main method which generate a ZipFile
			:returns: zipfile which is contains all the maps and metadatas
		"""
		self.fill_list_of_img()
		self.fill_list_of_metadata()
		self.intersect_list_image_metadata()
		zipFile = self.createZip()
		return zipFile

	def fill_list_of_img(self):
		"""
		fill the listOfImg with all the name of images in the directory path
		Take all the extension images exist in the list extension in UI generateMap (sort is make after with the metadataList)
		Take just the images in the root of directory path
		"""
		#Switch to the path from the parameters
		os.chdir(self.path)

		#Add each map to the list of map
		[self.listOfImg.append(file)
		for count in range(len(self.listOfExtensionImg))
		for file in glob.glob("*." + self.listOfExtensionImg.itemText(count))]

	def fill_list_of_metadata(self):
		"""
		fill the listOfMetadata with all the name of metadata in the directory path/metadata
		The metadata must in extension JSON
		Take just the images in the root of directory path/metadata
		"""
		#Switch to the metadata directory
		os.chdir(self.path+'/metadata') # TODO control if path exist
		#Add each file of metadata to the list of metadata
		[self.listOfMetadata.append(file) for file in glob.glob("*.json")]


	def intersect_list_image_metadata(self):
		"""
		remove all the metadata where images dosn't exists
		AND
		remove all the images where metadata dosn't exists
		A new list was created with the true name of images where have a metadata.
		The true list of metadata was implicit with the true list of images  
		"""
		#On supprime l'extension '.json' des metadata (les metadata on pour nom [nomDeLImage].[extImage].json)
		#et on intersect avec les vrais nom d'images
		#Remove json extension to each metadata files and we intersect each list to avoid map without metadata or metadata withou map
		self.listOfImgToArchive = set([os.path.splitext(x)[0] for x in self.listOfMetadata]).intersection(self.listOfImg)

	def createZip(self):
		"""
		This method create the zip with all the file in listOfImgToArchive
		:returns: the name of the zip
		"""
		#Initialize the logger
		logger = Logger()
		excludeMap = len(self.listOfImg) - len(self.listOfImgToArchive)
		excludeMeta = len(self.listOfMetadata) - len(self.listOfImgToArchive)
		# Exclude file generation_info
		excludeMeta -= 1
		if excludeMap > 0:
			logger.info(" Image(s) exclue(s) : " + str(excludeMap))

		if excludeMeta > 0:
			logger.info(" Metadonnée(s) exclue(s) : " + str(excludeMeta))

		#Creation of the zipfile
		fileName = self.path + '/' + self.nameZipFile + str(time.strftime("%Y%m%d%H%M%S"))  + ".zip"
		zipf = zipfile.ZipFile(fileName, 'w')
		for file in self.listOfImgToArchive:
			zipf.write(self.path + "/" + file, file) # Le fichier à exporter , le nom du fichier dans l'archive ZIP (surement pas correct mais ça marche !)
			zipf.write(self.path + "/metadata/" + file + ".json", "/metadata/" + file + ".json")

		zipf.close()
		return fileName


