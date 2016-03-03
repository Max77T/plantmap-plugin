# coding: utf8

from plantmap_engine import plantMapEngine
from IplantMapThread import PlantMapThreadInterface
from logger import *
from qgis_utils import QgisUtils

class deepValidation(PlantMapThreadInterface):
	"""
		This class make a deep research in the input layer to know exactly the status of a taxon.
		It replaces the subset filter with the input field and each value of the taxon board
	"""

	def __init__(self, layer, fieldName, whereEditable, description, taxonList):
		super(deepValidation, self).__init__()
		self.resultTaxonList = []
		self.layer = layer
		self.fieldName = fieldName
		self.whereEditable = whereEditable
		self.description = description
		self.pme = plantMapEngine()
		self.taxonList = taxonList
		self.timerInit(len(self.taxonList))



	def run(self):
		"""
			Main process of the class, put the result of research in a list which is return to the main thread
		"""
		try:
			#Logger
			self.logProgress.emit(Logger.INFO, u"=> Début du filtrage avancé <=")
			#Temporary list of taxons
			myListTaxon = []
			#Test if user filled the whereeditable field
			self.whereEditableWithAnd = self.whereEditable
			if self.whereEditableWithAnd != '':
				self.whereEditableWithAnd = " AND " + self.whereEditable

			#Iterating over each taxon that the user put into the list to generate
			for taxon in self.taxonList:
				self.timerNewTurn()
				self.timerNotify()
				if(self.isKilled() == True):
					break
				#Remove the quoto at the begining and the end of taxon's string
				#newTaxon = filter(lambda x: x != "'", taxon[0])
				if taxon[1] == None:
					#Make our own filter on the layer
					filterLayer = str(self.fieldName) +" = "+ taxon[0] + self.whereEditableWithAnd
	                #Apply the filter
					result = QgisUtils.set_subsetstring(self.layer, filterLayer)
					if result == False:
						self.logProgress.emit(Logger.ERROR, u"Filtre incorrect : " + str(filterLayer))
					#Get the description of the taxon according to the parameters
					desc = self.pme.get_description(taxon[0],self.layer,self.fieldName,self.description,self.whereEditable)
					if desc != None:
						t = (taxon[0], desc, "OK")
						myListTaxon.append(t)
					else:
						myListTaxon.append((taxon[0], desc, "NOK"))
				else:
					myListTaxon.append((taxon[0], taxon[1], "OK"))
			
			self.resultTaxonList = myListTaxon
			self.logProgress.emit(Logger.INFO, u"=> Fin du filtrage <=" )
			self.timerEnd()
		except Exception as e:
			self.logProgress.emit(Logger.ERROR, u"Echec de filtrage avancé : " + str(e))

	def getResult(self):
		"""
			Return the list of taxon with their status
			:returns: taxon list with status and description for each one
		"""
		return self.resultTaxonList

