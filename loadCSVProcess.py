# coding: utf8
import time
import glob, os
import zipfile
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox, QComboBox
from PyQt4.QtXml import QDomDocument
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from plantmap_engine import *
from IplantMapThread import *
from logger import *
import csv

class loadCSV(PlantMapThreadInterface):
	"""
		This class implement PlantMapThreadInterface which allow him to load a csv and extract the data trough a thread
	"""

	def __init__(self, csvFile, layer, iterationField, descriptionField, whereEditable):
		super(loadCSV, self).__init__()
		self.listTaxon = []
		self.csvFile = csvFile
		self.layer = layer
		self.iterationField = iterationField
		self.descriptionField = descriptionField
		self.whereEditable = whereEditable
		self.pme = plantMapEngine()


	def run(self):
		"""
			This method is the main process of the thread which load a csv and get the description of each data from the layer
		"""
		try:
			self.logProgress.emit(Logger.INFO, u"=> Début du chargement du fichier CSV <=")
			#Get the number of line to check in the csv file
			num_rows = sum(1 for line in open(self.csvFile))
			self.timerInit(num_rows)
			self.logProgress.emit(Logger.INFO, u"Nombre de taxon à charger : " + str(num_rows))
			if(self.isKilled() == True):
				return
			#Open the csv file
			with open(self.csvFile, 'rb') as csvfile:
				#Spamreader represent the cells in the first column
				spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
				#Iterating over each cell
				for row in spamreader:
					if(self.isKilled() == True):
						break
					#Initialize the progress bar
					self.timerNewTurn()                
					self.timerNotify()
					if row: 
						# get the description from the layer of the cell contents
						descriptionFeature = self.pme.get_description(row[0],self.layer,self.iterationField,self.descriptionField, self.whereEditable)
						if descriptionFeature != None:       
							self.listTaxon.append((row[0],descriptionFeature,"OK"))
						else:
							self.listTaxon.append((row[0],descriptionFeature,"NOK"))
				self.timerEnd()
				self.logProgress.emit(Logger.INFO, u"=> Fin du chargement <=" )
		except Exception as e:
			self.logProgress.emit(Logger.ERROR, u"Echec chargement fichier CSV :" + str(e))

	def getResult(self):
		"""
			Return the list from the main process with taxon and description
			:returns: List which contains tuples for each taxon (taxonID, decription)
		"""
		return self.listTaxon