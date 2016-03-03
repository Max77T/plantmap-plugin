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
import csv
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox
from PyQt4.QtXml import QDomDocument
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from qgis.core import *
from qgis.utils import*
import threading
import time
from datetime import datetime

from export import *
from mapgenerator import *
from plantmap_engine import *
from generationData import *
from metadata_writer import *
from plantMapXML import *
from project import *
from PyQt4 import uic
from logger import *

from plantmap_progress import PlantMapProgress
from handlers import *

from deepValidationProcess import *
from IexternalProcessThread import *
from loadCSVProcess import loadCSV
import plantmap_dialog_base #import Ui_PlantMapDialogBase

class PlantMapDialog(QtGui.QDialog, plantmap_dialog_base.Ui_PlantMapDialogBase):
    def __init__(self,parent):
        """Constructor"""
        QtGui.QDialog.__init__(self)

        #Constructor of the engine to check the existance of the taxon
        self.pme = plantMapEngine()
        self.pxml = plantMapXML()

        self.iface = parent
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        self.setupUi(self)

        logger = Logger()
        logger.addOutput(TextEditHandler(self.UI_logViewPlugin))
        self.taxonList=[]
        self.projectXML = None
        self.fromEdit = False
        self.listMetadataToCreate = []


        ### ---- Regex for each field --- ###
        regexp = QtCore.QRegExp('([^@]+@[^@]+\.[^@]+)')
        validator = QtGui.QRegExpValidator(regexp)
        #Email
        self.UI_contactEmail.setValidator(validator)

        regexpfilename = QtCore.QRegExp('[a-zA-Z0-9_]*')
        validatorName = QtGui.QRegExpValidator(regexpfilename)
        #Mapname 
        self.UI_mapName.setValidator(validatorName)

        regexppath = QtCore.QRegExp('[a-zA-Z0-9_\\\/\:]*')
        validatorName = QtGui.QRegExpValidator(regexppath)
        #path 
        self.UI_storagePath.setValidator(validatorName)
        self.UI_exportPath.setValidator(validatorName)

        #### ---- Navigation into the interface of edition and creation of project ---- ####
        self.UI_buttonCreateProject.clicked.connect(self.test_sender)
        self.UI_buttonCreate.clicked.connect(self.validate_project_creation)
        self.UI_buttonPrevious.clicked.connect(self.prev)
        self.UI_taxonID.returnPressed.connect(self.validate_taxon)
        self.UI_buttonPrevious.clicked.connect(self.put_to_false)
        self.UI_buttonCreateProjectFrom.clicked.connect(self.next2)
        self.UI_buttonEditProject.clicked.connect(self.next2)
        self.UI_validationProject.clicked.connect(self.valide_select_project)
        self.UI_comboProjectSelection.currentIndexChanged.connect(self.fill_project_tab)
        self.tabWidget.currentChanged.connect(self.set_project_selection_combobox)
        self.UI_cancelProject.clicked.connect(self.prev2)
        self.UI_cancelProject.clicked.connect(self.put_to_false)
        self.UI_deepValidation.clicked.connect(self.deep_validation)
        self.UI_exportButton.clicked.connect(self.validate_export)
        self.UI_projectName.textChanged.connect(self.check_state_project_name)
        self.UI_projectDescription.textChanged.connect(self.check_state_description)
        self.UI_contactName.textChanged.connect(self.check_state)
        self.UI_contactEmail.textChanged.connect(self.check_state_email)
        self.UI_startDate.dateChanged.connect(self.check_state_date)
        self.UI_endDate.dateChanged.connect(self.check_state_date)
        self.UI_projectVersion.textChanged.connect(self.check_state)
        self.UI_mapName.textChanged.connect(self.check_state_map_name)
        self.UI_storagePath.textChanged.connect(self.check_state_map_name)
        self.UI_exportPath.textChanged.connect(self.check_state_map_name)
        self.UI_projectName.textChanged.emit(self.UI_projectName.text())
        self.UI_contactName.textChanged.emit(self.UI_contactName.text())
        self.UI_contactEmail.textChanged.emit(self.UI_contactEmail.text())
        self.UI_projectVersion.textChanged.emit(self.UI_projectVersion.text())
        self.UI_storagePath.textChanged.emit(self.UI_storagePath.text())
        self.UI_mapName.textChanged.emit(self.UI_mapName.text())
        self.UI_exportPath.textChanged.emit(self.UI_exportPath.text())
        #### Check if the user complete each field ####
        self.UI_validateTaxonID.clicked.connect(self.validate_taxon)
        self.UI_generateMapButton.clicked.connect(self.validate_map_generation)
        #### Remove a taxon
        self.UI_buttonRemoveAll.clicked.connect(self.validate_remove_all)
        self.UI_storagePathButton.clicked.connect(self.stockage_file_dialog)
        self.UI_validateTaxonList.clicked.connect(self.taxon_list_file_dialog)
        self.UI_exportPathButton.clicked.connect(self.export_file_dialog)
        self.UI_whereEditable.editingFinished.connect(self.check_where_editable)

    """
        Navigation into the project tab
    """
    def next(self):
        i = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(i + 1)               

    def prev(self):
        i = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(i - 1)
        if self.sender() == self.UI_validationProject:
            self.fill_project_field()


    def next2(self):
        i = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(i + 2)
        if self.sender() == self.UI_buttonEditProject:
            self.fromEdit = True
        self.select_project(self.UI_comboProjectSelection)
        # self.fill_project_tab()

    def prev2(self):
        i = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(i - 2)



    def check_where_editable(self):
        """
        Check if the Where editable is syntactically correct
        """

        filterWhere = self.UI_whereEditable.text()
        if filterWhere == '':
            self.UI_whereEditable.setStyleSheet('QLineEdit { background-color: %s }' % '#ffffff')
        else:
            self.UI_whereEditable.setStyleSheet('QLineEdit { background-color: %s }' % '#AEEEEE')
            
        """
        Doesn't work with the new OGR type date : cast("FieldDAte" as character) > 'yyy-mm-dd'
        """
        # exp = QgsExpression(filterWhere)
        # print exp.parserErrorString()
        # if exp.hasParserError() == True:
        #     self.UI_whereEditable.setStyleSheet('QLineEdit { background-color: %s }' % '#f6989d')
        # else:
        #     self.UI_whereEditable.setStyleSheet('QLineEdit { background-color: %s }' % '#c4df9b')


    def check_state_map_name(self):
        sender = self.sender()
        validator = sender.validator()
        state = validator.validate( os.path.basename(os.path.normpath(sender.text())),0)[0]
        if state == QtGui.QValidator.Acceptable and sender.text() != '':
            color = '#c4df9b' # green
        else:
            color = '#f6989d' # red
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def check_state_date(self):
        sender = self.sender()
        if self.UI_endDate.date() < self.UI_startDate.date():
            color = '#f6989d' # red
        else:
            color = '#c4df9b' # green
        self.UI_startDate.setStyleSheet('QDateEdit { background-color: %s }' % color)
        self.UI_endDate.setStyleSheet('QDateEdit { background-color: %s }' % color)

    def check_state(self):
        sender = self.sender()
        if sender.text() =='':
            color = '#f6989d' # red
        else:
            color = '#c4df9b' # green
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def check_state_description(self):
        sender = self.sender()
        if sender.toPlainText()=='':
            color = '#f6989d' # red
        else:
            color = '#c4df9b' # green
        sender.setStyleSheet('QPlainTextEdit { background-color: %s }' % color)


    def check_state_email(self):
        sender = self.sender()
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QtGui.QValidator.Acceptable:
            color = '#c4df9b' # green
        else:
            color = '#f6989d' # red
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)


    def check_state_project_name(self):
        sender = self.sender()
        projects = self.pme.get_project()
        if self.fromEdit == False:
            if self.pme.check_project_name(projects,sender.text().strip()) or sender.text() == '':
                color = '#f6989d' # red
            else:
                color = '#c4df9b' # green
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
        else:
            color = '#c4df9b'
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
                    
    def put_to_false(self):
        """
            This method put to false to know
            if the creation project come from the button of creation with an other one or from the button edit project
        """
        self.fromEdit = False
        self.UI_projectName.setReadOnly(False)


    def deep_validation(self):
        """
            Make the deep validation
        """
        # Check if taxon board is empty
        if self.get_size() < 0:
            return
        else:
            #Put the process into a thread worker
            externalProcess = deepExternalProcessValidation(self.UI_taxonLayer.itemData(self.UI_taxonLayer.currentIndex()))
            self.myLongTask = deepValidation(self.UI_taxonLayer.itemData(self.UI_taxonLayer.currentIndex()),
                self.UI_iterationField.currentText(),
                self.UI_whereEditable.text(),
                self.UI_descriptionField.currentText(),
                self.taxonList)
            #Initialize the thread
            self.dia = PlantMapProgress(self.myLongTask, externalProcess)
            #Run the threah
            self.dia.exec_()

            # Get the result of the thread
            listResult = externalProcess.taxonList
            # Remove the current content of the taxon board
            self.validate_remove_all()
            # Put the new taxon from the deep validation with their exact description
            for taxonTuple in listResult:
                self.add_Taxon_To_Board(taxonTuple[0], taxonTuple[1], taxonTuple[2])


    def stockage_file_dialog(self):
        """
            This method allow the user to select a directory through the OS system file to save the map from the generation
        """
        self.UI_storagePath.setText(QFileDialog.getExistingDirectory())


    def taxon_list_file_dialog(self):
        """
            This method allow the user to select a file through the OS system file
        """
        pathFile = QFileDialog.getOpenFileName()
        if not pathFile == '':

            #The process is done in a thread
            externalProcess = loadCSVExternalProcess()

            myLongTask = loadCSV(pathFile, 
                self.UI_taxonLayer.itemData(self.UI_taxonLayer.currentIndex()), 
                self.UI_iterationField.currentText(),
                self.UI_descriptionField.currentText(),
                self.UI_whereEditable.text(),
                self.check_isString(self.UI_iterationField.currentText(), self.UI_taxonLayer.itemData(self.UI_taxonLayer.currentIndex()))
                )

            self.dia = PlantMapProgress(myLongTask, externalProcess)
            self.dia.exec_()

            listResult = externalProcess.taxonList
            for taxonTuple in listResult:
                self.add_Taxon_To_Board(taxonTuple[0], taxonTuple[1], taxonTuple[2])

    def export_file_dialog(self):
        """
            This method allow the user to select a directory through the OS system file to save the zip from the export 
        """
        self.UI_exportPath.setText(QFileDialog.getExistingDirectory())

    def export(self):
        """
            Export process
        """
        export = Export(self.UI_exportPath.text(), self.UI_extensionMap) # TODO
        export.process()
        QMessageBox.information(self,
            self.trUtf8("Export"),
            self.trUtf8("Export terminé"))


    def select_project(self,comboboxToFill):
        """
            This method add all project to the combobox and call fill_project_tab
        """
        projectList = self.pme.get_project()
        comboboxToFill.clear()
        comboboxToFill.addItems(projectList)
        
    def set_project_selection_combobox(self):
        self.select_project(self.UI_projectSelection)

    """
    ***************************************************************************
        TAB PROJECT
    ***************************************************************************
    """

    def test_sender(self):
        """
            This method determine which button called the description form :
                - create project
                - create project from an other one
            If it's the first one, it's clear all the field otherwise do something in prev
        """
        if self.sender() == self.UI_buttonCreateProject:
            self.UI_projectName.clear()
            self.UI_projectDescription.clear()
            self.UI_contactName.clear()
            self.UI_contactEmail.clear()
            self.UI_cbnOrganisation.setCurrentIndex(0)
            self.UI_startDate.setDate(QDate.currentDate())
            self.UI_endDate.setDate(QDate.currentDate())
            self.UI_projectVersion.clear() # Peut être ajouter un compteur
            self.UI_thesaurusISO.setCurrentIndex(0)
            self.UI_thesaurusInspire.setCurrentIndex(0)
            self.UI_keywords.clear()
            self.UI_contact.clear()
            self.UI_dataOwner.clear()
            self.UI_genealogyData.clear()
            self.UI_cbnManager.clear() # change to combobox
            self.UI_updateFrequency.clear()
            self.UI_usageLimit.clear()
            self.UI_dataState.clear()
            self.next()
        else:
            self.prev()
            
    def valide_select_project(self):
        """
            This method control if the user has selected a project before to continue
        """
        if self.UI_comboProjectSelection.currentText() == '':
            self.error_message("Veuillez créer un projet")
            return
        else:
            self.projectXML = self.get_project_from_xml()
            self.test_sender()

    def get_project_from_xml(self):
        """
            This method construct the xml project and return this one
            :returns: return the project object
        """
        tmpProject = Project(self.UI_displayProjectName.text(), # name
            self.UI_displayProjectDescription.text(), # description
            self.UI_tabProject.item(0,1).text(), # contactName
            self.UI_tabProject.item(1,1).text(), # contactEmail
            self.UI_tabProject.item(2,1).text(), # cbnOrganisation
            self.UI_tabProject.item(3,1).text(), # studyStartDate
            self.UI_tabProject.item(4,1).text(), # studyEndDate
            self.UI_tabProject.item(5,1).text(), # projectVersion
            self.UI_tabProject.item(7,1).text(), # thesaurusISO
            self.UI_tabProject.item(8,1).text(), # thesaurusInspire
            self.UI_tabProject.item(16,1).text().split(','), # keywords
            self.UI_tabProject.item(9,1).text(), # contact
            self.UI_tabProject.item(10,1).text(), # dataOwner
            self.UI_tabProject.item(11,1).text(), # genealogyData
            self.UI_tabProject.item(12,1).text(), # cbnManager
            self.UI_tabProject.item(13,1).text(), # updateFrequency
            self.UI_tabProject.item(14,1).text(), # usageLimitation
            self.UI_tabProject.item(15,1).text(), # dataState
            self.UI_tabProject.item(6,1).text()  # dateModification
            )   
        return tmpProject

    def validate_project_creation(self):
        """
            This method check if the project form is properly complete
            :returns: return if a condition isn't respected
        """
        #Check each field
        if self.UI_projectName.text() == '':
            self.error_message("Veuillez renseigner un nom de projet")
            return
        if self.fromEdit == False:
            if self.pme.check_project_name(self.pme.get_project(),self.UI_projectName.text()):
                self.error_message("Nom de projet déjà existant")
                return
        if self.UI_projectDescription.toPlainText() == '':
            self.error_message("Veuillez renseigner une description de projet")
            return
        if self.UI_contactName.text() == '':
            self.error_message("Veuillez renseigner un contact")
            return
        if self.UI_contactEmail.text() == '':
            self.error_message("Veuillez renseigner un email de contact")
            return
        if self.UI_projectVersion.text() == '':
            self.error_message("Veuillez renseigner une version de projet")
            return
        if self.UI_endDate.date() < self.UI_startDate.date():
            self.error_message("Veuillez renseigner une période d'étude valide (date de fin > date de début)")
            return

        # Project object 
        project = Project(
            self.UI_projectName.text().strip(),
            self.UI_projectDescription.toPlainText(),
            self.UI_contactName.text(),
            self.UI_contactEmail.text(),
            self.UI_cbnOrganisation.currentText(),
            self.UI_startDate.date(),
            self.UI_endDate.date(),
            self.UI_projectVersion.text(),
            self.UI_thesaurusISO.currentText(),
            self.UI_thesaurusInspire.currentText(),
            self.pme.parsingKeyWords(self.UI_keywords.text()),
            self.UI_contact.text(),#TODO, changer dans l'UI par UI_contactInspire
            self.UI_dataOwner.text(),
            self.UI_genealogyData.text(),
            self.UI_cbnManager.text(),
            self.UI_updateFrequency.text(),
            self.UI_usageLimit.text(),
            self.UI_dataState.text(),
            str(time.strftime("%Y-%m-%d")))

        # Put to false cause here we don't come from edit button
        self.put_to_false()
        # Write xml project
        self.pxml.xml_writer(project)
        self.prev()


    def fill_project_field(self):

        """
            Fill each field from the project creation form when it's called from the selection form 
        """


        if self.fromEdit == True:        
            self.UI_projectName.setText(self.projectXML.name)
            self.UI_projectName.setReadOnly(True)
            self.UI_projectDescription.clear()
            self.UI_projectDescription.insertPlainText(self.projectXML.description)
        else:
            self.UI_projectName.clear()
            self.UI_projectDescription.clear()

        self.UI_contactName.setText(self.projectXML.contactName)
        self.UI_contactEmail.setText(self.projectXML.contactEmail)

        index = self.UI_cbnOrganisation.findText(self.projectXML.cbnOrganisation, QtCore.Qt.MatchFixedString)
        self.UI_cbnOrganisation.setCurrentIndex(index)

        dateS = datetime.strptime(self.projectXML.studyStartDate,"%Y-%m-%d")
        dateE = datetime.strptime(self.projectXML.studyEndDate,"%Y-%m-%d")
        self.UI_startDate.setDate(dateS)
        self.UI_endDate.setDate(dateE)

        self.UI_projectVersion.setText(self.projectXML.projectVersion)

        indexISO = self.UI_thesaurusISO.findText(self.projectXML.thesaurusISO,QtCore.Qt.MatchFixedString)
        self.UI_thesaurusISO.setCurrentIndex(indexISO)

        indexInspire = self.UI_thesaurusInspire.findText(self.projectXML.thesaurusInspire,QtCore.Qt.MatchFixedString)
        self.UI_thesaurusInspire.findData(indexInspire)

        self.UI_keywords.setText(','.join(self.projectXML.keywords))
        self.UI_contact.setText(self.projectXML.contactInspire)
        self.UI_dataOwner.setText(self.projectXML.dataOwner)
        self.UI_genealogyData.setText(self.projectXML.genealogyData)
        self.UI_cbnManager.setText(self.projectXML.cbnManager)
        self.UI_updateFrequency.setText(self.projectXML.updateFrequency)
        self.UI_usageLimit.setText(self.projectXML.usageLimitation)
        self.UI_dataState.setText(self.projectXML.dataState)


    def fill_project_tab(self):
        """
            This method populate the description project tab from an xml
        """
        #Avoid the case of an empty combobox
        if self.UI_comboProjectSelection.currentText() == '':
            return
        root = self.pme.get_all_field_from_project(self.UI_comboProjectSelection.currentText())   

        projectTab = self.UI_tabProject
       
        # Initialize the taxon board
        self.UI_tabProject.setRowCount(19)
        self.UI_tabProject.setColumnCount(2)

        self.UI_displayProjectName.clear()
        self.UI_displayProjectDescription.clear()

        i = 0
        # Add each xml object of the xml file into the taxon board
        for child in root:
            
            if(child.tag == "projectName"):
                self.UI_displayProjectName.setText(unicode(child.text))
            elif(child.tag == "description"):
                self.UI_displayProjectDescription.setText(unicode(child.text))
            elif(child.tag == "keywords"):
                projectTab.setItem(i,0,QtGui.QTableWidgetItem(child.tag))
                words = ""
                for word in child:
                    if words != "":
                        words = words + ","+ word.text
                    else:
                        words = words + (word.text if word.text else "")
                projectTab.setItem(i,1,QtGui.QTableWidgetItem(words))
                i=i+1
            else:  
                projectTab.setItem(i,0,QtGui.QTableWidgetItem(child.tag))
                projectTab.setItem(i,1,QtGui.QTableWidgetItem(child.text))
                i=i+1
            



    """
    ***************************************************************************
        TAB GENERATION
    ***************************************************************************
    """



    def validate_export(self):
        """
        This method check if the export file has been filled
        """
        if self.UI_exportPath.text() == '' or self.UI_exportPath.validator().validate(os.path.basename(os.path.normpath(self.UI_exportPath.text())), 0)[0] == QtGui.QValidator.Invalid:
            self.error_message("Veuillez sélectionner un chemin (le dossier final ne peut contenir que des caractères du type : [a-zA-Z0-9])")
            return
        if not os.path.exists(self.UI_exportPath.text() + '/metadata'):
            self.error_message("Votre dossier ne contient pas de dossier 'metadata'")
            return
        self.export()

    def validate_taxon(self):
        """
        This method check if the ID taxon is not empty
        """

        #Catch the text in a local variable
        inputTaxonID = self.UI_taxonID.text()
        layer = self.UI_taxonLayer.itemData(self.UI_taxonLayer.currentIndex())
        iterationField = self.UI_iterationField.currentText()
        descriptionField = self.UI_descriptionField.currentText()
        whereEditable = self.UI_whereEditable.text()

        if inputTaxonID == '': #Pas de retourne dans ce cas la !
            self.error_message("Veuillez indiquer un ID de taxon")
        else:
            #If the taxon name have a qote, you need to double qote (for the filter)
            newTaxon = inputTaxonID.replace("'", "''")
            if self.check_isString(self.UI_iterationField.currentText(), self.UI_taxonLayer.itemData(self.UI_taxonLayer.currentIndex())) == True:
                newTaxon = "'" + newTaxon + "'"
            descriptionFeature = self.pme.get_description(newTaxon,layer,iterationField,descriptionField, whereEditable)

            if descriptionFeature != None:
                self.add_Taxon_To_Board(newTaxon,descriptionFeature,"OK")
            else:
                self.add_Taxon_To_Board(newTaxon,descriptionFeature,"NOK")


            """
            **************************************************
                TAB GENERATION  : TAXON TAB
            **************************************************
            """
    def validate_remove_all(self):
        """
            This method check if the board is empty, if not remove all the taxon
        """
        if self.get_size() > 0:
            for i in reversed(range(self.UI_taxonTab.rowCount())):
                self.UI_taxonTab.removeRow(i)
            del self.taxonList[:]
        else:
            self.error_message("Le tableau de taxons est déjà vide")

    def validate_map_generation(self):
        """
        This method control if all the field are filled. If they do then plugin start the map generation
        If they aren't filled so the plugin display an error message.
        """

        if self.UI_storagePath.text() == '' or self.UI_exportPath.validator().validate(os.path.basename(os.path.normpath(self.UI_storagePath.text())), 0)[0] == QtGui.QValidator.Invalid:
            self.error_message("Un lieu de stockage doit être préciser (les dossiers ne peuvent contenir que des caractères du type : [a-zA-Z0-9])")
            return
        if self.UI_taxonTab.rowCount() == 0:
            self.error_message("Aucun taxon renseigné, Veuillez importer une liste de taxon ou un taxon")
            return
        if self.UI_projectSelection.currentText() == '':
            self.error_message("Veuillez créer un projet et le sélectionner avant de générer des cartes")
            return
        if self.UI_taxonLayer.currentText() == '':
            self.error_message("Veuillez ajouter une couche avant de générer des cartes")
            return
        if self.UI_iterationField.currentText() == '':
            self.error_message("Veuillez ajouter une couche avec des champs itérables")
            return
        if self.UI_composerName.currentText() == '':
            self.error_message("Veuillez créer et sélectionner un composer avant de générer des cartes")
            return
        if self.UI_mapName.text() == '':
            self.error_message("Veuillez indiquer un nom de carte en sortie")
            return

        # Create the list of taxon to generate (without the incorrect taxon)
        listToGenerate = filter(lambda taxon: taxon[1] != None,self.taxonList)
        # Put into a genData object all data for the generation
        genData = generationData(self.UI_projectSelection,
            self.UI_mapName,
            self.UI_taxonLayer.itemData(self.UI_taxonLayer.currentIndex()),
            self.UI_iterationField,
            self.UI_storagePath,
            listToGenerate,
            self.UI_composerName.itemData(self.UI_composerName.currentIndex()),
            self.UI_extensionMap,
            self.UI_whereEditable)
        # Get all metadata to generate from the xml file (project)
        root = self.pme.get_all_field_from_project(self.UI_projectSelection.currentText())
        # Put all metadata into a list
        self.listMetadataToCreate = self.pme.load_xml(root)
        # map generation 
        self.generate(genData)
        

    def add_Taxon_To_Board(self,taxonID,description,status):
        """
        Add a taxon to the list from the text input previously tested
        :param taxonID: the id taxon
        :param description: description of a taxon from the field descriptionField
        :param status: put a status of a taxon if present or not
        :returns: True, if a taxon has been added to the list and false if not
        """

        # Get the taxon list
        taxonBoard = self.UI_taxonTab
        taxonBoardCount = self.get_size()

        # Add ' ' or not according to the type of the field
        # concatTaxon = self.check_type(self.UI_iterationField.currentText(),
        #     self.UI_taxonLayer.itemData(self.UI_taxonLayer.currentIndex()),
        #     taxonID)
        concatTaxon = taxonID
        #Test if a taxon is already in the list of taxon
        for item, v in enumerate(self.taxonList):
            if v[0] == concatTaxon:
                QMessageBox.warning(self,
                self.trUtf8("Intégration d'un taxon à la liste"), #indiquer plutôt que le taxon est déjà dans la liste ?
                self.trUtf8(str(concatTaxon)+" déjà présent dans le tableau"))
                return False


        taxonBoard.setSortingEnabled(False)
        # Set the properties of the taxon list
        taxonBoard.setRowCount(taxonBoardCount+1)
        taxonBoard.setColumnCount(4)

        # Set the input text to empty
        self.UI_taxonID.setText(u'')

        #Add the new taxon item to the table
        newTaxon = QTableWidgetItem()
        newTaxon.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
        newTaxon.setData( Qt.EditRole,concatTaxon )
        taxonBoard.setItem(taxonBoardCount,0,newTaxon)


        # Add the description from the field of the layer
        newDescription = QTableWidgetItem()
        newDescription.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
        newDescription.setData(Qt.EditRole,description)
        taxonBoard.setItem(taxonBoardCount,1,newDescription)

        # Add the status from the result of the check in layer source
        newStatus = QTableWidgetItem()
        newStatus.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
        newStatus.setData(Qt.EditRole,status)
        taxonBoard.setItem(taxonBoardCount,2,newStatus)

        # Add a remove button in the taxon board
        btnRemove = QPushButton(taxonBoard)
        btnRemove.setText("Supprimer")
        # brnRemove.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
        # brnRemove.setData(Qt.EditRole,status)
        btnRemove.clicked.connect(self.handler_remove_button)
        taxonBoard.setCellWidget(taxonBoardCount,3,btnRemove)
        

        taxonBoard.setSortingEnabled(True)
        # Add taxon
        t =  (concatTaxon,description)
        self.taxonList.append(t)

        return True

    def get_size(self):
        """
            Get the size of the taxonList
            :returns: The size of the tab
        """
        taxonBoardCount = self.UI_taxonTab.rowCount()
        return taxonBoardCount

    def handler_remove_button(self):
        """ 
        Remove a taxon thanks to the button in the taxon board
        """
        # Remove the taxon from the list
        #button = QtGui.qApp.focusWidget()
        button = self.sender()
        # Add the process to the remove button of the taxon board for each taxon
        index = self.UI_taxonTab.indexAt(button.pos())
        output = filter(lambda x: x[0]!=self.UI_taxonTab.item(index.row(),0).text(),self.taxonList)
        self.taxonList = output
        self.UI_taxonTab.removeRow(index.row())
        self.UI_taxonTab.viewport().update()
    

    def check_type(self,iterationField,layer,taxonID):
        """
            This method check if the field of iteration is a string and put quote at the start & end of the taxonID to request the layer
            :params iterationField: field of iteration
            :params layer: layer which has been selected by the user
            :params taxonID: represents the id taxon extract from the iterationField 
            :returns: return the taxon with quote if iterationField is a string type or without if not
        """
        iterationFieldType = layer.pendingFields().field(iterationField).type()
        if iterationFieldType == 10:
            return "'"+taxonID+"'"
        else:
            return taxonID

    def check_isString(self,iterationField,layer):
        """
            This method check if the field of iteration is a string and put quote at the start & end of the taxonID to request the layer
            :params iterationField: field of iteration
            :params layer: layer which has been selected by the user
            :params taxonID: represents the id taxon extract from the iterationField 
            :returns: return the taxon with quote if iterationField is a string type or without if not
        """
        iterationFieldType = layer.pendingFields().field(iterationField).type()
        if iterationFieldType == 10:
            return True
        else:
            return False



    def remove_Taxon_From_Board(self):
        """
        Remove a taxon from the list if a row is selected
        When the users clicks on the remove button
        """

        #Get selected lines
        taxonBoard = self.UI_taxonTab   
        sm = taxonBoard.selectionModel()
        lines = sm.selectedRows()
        if not lines or len(lines) != 1:
            return

        row = lines[0].row()

        #Get taxon id
        taxonID = taxonBoard.item(row,0).data(Qt.EditRole)

        # Remove the taxon from the list
        self.taxonList.remove(taxonID)

        # Update project
        p = QgsProject.instance()
        p.writeEntry( 'PluginPlantMap', 'taxonList', self.taxonList )
        p.setDirty( True )

        # Remove selected taxons
        taxonBoard = self.UI_taxonTab
        taxonBoard.removeRow(taxonBoard.currentRow())
        taxonBoard.setRowCount(self.get_size()-1)
    

    def error_message(self,message):
        """
        This method display a message to the user with the origin of the error
        """
        QMessageBox.critical(self,
            self.trUtf8("Génération impossible"),
            self.trUtf8(message))

    def en_of_generate(self):
         QMessageBox.critical(self,
            self.trUtf8("Génération"),
            self.trUtf8("Génération terminée"))

    def generate(self, genData):
        """
            Launch the generation process through a thread
        """
        
        externalProcess = generatorMapExternalProcess(genData.layer)
        self.myLongTask = GeneratorMap(genData, self.listMetadataToCreate)
        self.dia = PlantMapProgress(self.myLongTask, externalProcess, genData.storagePath.text())
        self.dia.exec_()

        

       
