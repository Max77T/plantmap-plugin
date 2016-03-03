# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PlantMapDialog
                                 A QGIS plugin
 This plugin provide a genertor of multitude maps
                             -------------------
        begin                : 2015-11-23
        git sha              : $Format:%H$
        copyright            : (C) 2015 by GreenMapper
        email                : maxencebunel77@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import logging
import json
import sys
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
from datetime import datetime
from plantMapXML import *

class plantMapEngine():


	def __init__(self):
		self.iface = iface



	def get_description(self, taxonID, layer, iterationField,description, whereEditable):
		"""
		Check if the taxon id exits in the database or shapefile
		:param taxonID: the id of the taxon from the input text edit
		:return: return the description if the id taxon exits in the layer, or return an empty string if the description is empty
				, otherwise return None
		"""
		if whereEditable != '':
			whereEditable = " AND " + whereEditable
		#Create the expression to request to get the description of a taxon
		exp = QgsExpression(str(iterationField) + " = " + taxonID + whereEditable)
		#Transform expression to a request
		request = QgsFeatureRequest(exp)
		#Get features for the request
		features = layer.getFeatures(request)
		isPresent = False
		for feature in features:
			isPresent = True
			if not isinstance(feature[description],QPyNullVariant):
				#Return the description if find
				return feature[description]
		
		if isPresent == True:
			#Return '' cause in the layer there is no text
			return ''
		
		#Taxon not found
		return None

	def project_path(self):
		"""
			Return the directory which contains all projects
		"""
		return os.path.dirname(__file__)+'/project/'

	def get_project(self):
		"""
			Return all projects
		"""
		#XML object
		pxml = plantMapXML()
		path = self.project_path()
		projectList = []
		# Get all project from the directory
		for aFile in os.listdir(path):
			if aFile.endswith(".xml"):
				filePath = str(path+aFile)
				xmlFile = pxml.parse_xml(filePath)
				for projectName in xmlFile.iter('projectName'):
					projectList.append(projectName.text)

		return projectList

	def get_all_field_from_project(self, projectSelected):
		"""
			return all element from a xml project file
		"""
		pxml = plantMapXML()
		path = self.project_path()
		filePath = path+ unicode(projectSelected).encode("utf-8")
		xmlFile = pxml.parse_xml(filePath+'.xml')
		return xmlFile

	def check_project_name(self, projectNameList, name):
		"""
			Check if a name is a project
		"""
		return name in projectNameList


	def parsingKeyWords(self, keywords):
		"""
			Returns a splitted list of keywords
		"""
		words = keywords.split(',')
		return words

	def edit_taxon_tab(self,description,taxonTab,taxonID):
		"""
			Allow to modify a row according to the taxonID
		"""
		row = taxonTab.findItems(str(taxonID),Qt.MatchExactly)
		itemDesc = QTableWidgetItem(description)
		itemStatus = QTableWidgetItem("OK")
		taxonTab.setItem(row[0].row(),1,itemDesc)
		taxonTab.setItem(row[0].row(),2,itemStatus)

	def load_xml(self,root):
		"""
			This method load a xml file and return a list which contains all metadata
		"""
		loadXML = []
		for child in root:
			if(child.tag == "keywords"):
				words = ""
				for word in child:
					if words != "":
						words = words + "," + unicode(word.text)
					else:
						words = unicode(word.text)
				t = (child.tag,words)
				loadXML.append(t)
			else:
				t = (child.tag,child.text)
				loadXML.append(t)

		return loadXML

class ObjectJSON:
    def to_JSON(self):
    	"""
    		Return a json structure delimited by ',' and ':'
    	"""
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4, separators=(',',':'))
        