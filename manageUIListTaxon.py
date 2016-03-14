# coding: utf8

import os
import sys
import logging
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox
from PyQt4.QtXml import QDomDocument
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from qgis.core import *
from qgis.utils import*
from PyQt4 import uic



class ManageUIListTaxon(QObject):
	"""
	Manage all the taxon in the UI list and in the list for generation
	This class is an singleton, but the singleton fonctionnalities are not used for the moment.
	"""
	instance = None
	def __new__(cls):
		if cls.instance is None:
			cls.instance = QObject.__new__(cls)
		return cls.instance

	def __init__(self):
		super(ManageUIListTaxon, self).__init__()

	def initManager(self, taxonBoard):
		"""
		init the class with the UI object
		and init the coumpter
		"""
		self.taxonBoard = taxonBoard
		self.tmpList = []
		self.numberOfTaxon = 0
		self.numberOfTaxonInUIList = 0
		self.taxonBoard.setColumnCount(4)

		self.taxonList = []
		self.taxonDouble = []

	def getListOfTaxon(self):
		"""
		return a copy of list of taxon present in UI list
		"""
		return self.taxonList[:]

	def addTaxon(self, taxon, description, status):
		"""
		Add a taxon ... !
		But juste create a list in memory with ui objects. Not added in true in UI
		The method refresh added in UI !
		"""

		#Create a list of doubles taxon in List
		#this list is return by the method refreshTaxonTab
		#With that, you can add a list/multiple taxon, after you refresh the list, and make juste one warning with all doublon
		for item, v in enumerate(self.taxonList):
			if v[0] == taxon:
				self.taxonDouble.append(taxon)
				return

		newTaxon = QTableWidgetItem()
		newTaxon.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
		newTaxon.setData( Qt.EditRole,taxon)

		newDescription = QTableWidgetItem()
		newDescription.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
		newDescription.setData(Qt.EditRole,description)

		newStatus = QTableWidgetItem()
		newStatus.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
		newStatus.setData(Qt.EditRole,status)

		btnRemove = QPushButton(self.taxonBoard)
		btnRemove.setText("Supprimer")
		# brnRemove.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
		# brnRemove.setData(Qt.EditRole,status)
		btnRemove.clicked.connect(self.handler_remove_button)

		self.tmpList.append((newTaxon,newDescription, newStatus,btnRemove))
		self.numberOfTaxon += 1

		self.taxonList.append((taxon,description))

	def refreshTaxonTab(self):
		"""
		Uptodate the taxon UI tab.
		"""
		self.taxonBoard.setSortingEnabled(False)
		i = self.numberOfTaxonInUIList
		self.taxonBoard.setRowCount(self.numberOfTaxon) # allocation memory juste one time with all memory you need
		for taxonTuple in self.tmpList: #and added the taxon in UI
			self.taxonBoard.setItem(i,0,taxonTuple[0])
			self.taxonBoard.setItem(i,1,taxonTuple[1])
			self.taxonBoard.setItem(i,2,taxonTuple[2])
			self.taxonBoard.setCellWidget(i,3,taxonTuple[3])
			i += 1
			self.numberOfTaxonInUIList += 1
		self.taxonBoard.setSortingEnabled(True)
		self.tmpList = []

		tmpDoublon = self.taxonDouble
		self.taxonDouble = []
		return tmpDoublon


	def removeAll(self):
		"""
		Remove the list of taxon
		"""

		if self.numberOfTaxonInUIList > 0:
			for i in reversed(range(self.numberOfTaxonInUIList)):
				self.taxonBoard.removeRow(i)
			del self.taxonList[:]

			self.numberOfTaxon = 0
			self.numberOfTaxonInUIList = 0
			self.taxonList = []
		else:
			return False


	def handler_remove_button(self):
		""" 
		Remove a taxon thanks to the button in the taxon board
		"""
		# Remove the taxon from the list
		# button = QtGui.qApp.focusWidget()
		button = self.sender()
		# Add the process to the remove button of the taxon board for each taxon
		index = self.taxonBoard.indexAt(button.pos())
		output = filter(lambda x: x[0]!=self.taxonBoard.item(index.row(),0).text(),self.taxonList)
		self.taxonList = output
		self.taxonBoard.removeRow(index.row())
		self.taxonBoard.viewport().update()
		self.numberOfTaxon -= 1
		self.numberOfTaxonInUIList -= 1
