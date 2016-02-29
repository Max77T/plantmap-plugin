# coding: utf8

import json
from metadata_writer import MetadataWriter
from datetime import datetime
import os
from logger import *
from handlers import *
import csv
from IplantMapThread import PlantMapThreadInterface
from qgis_utils import QgisUtils
from plantmap_engine import ObjectJSON

class GenerateException(Exception):
    def __init__(self,raison):
        self.raison = raison
    
    def __str__(self):
         return self.raison




class GeneratorMap(PlantMapThreadInterface):
    """
    This class is a Thread for generate all the map.
    The field 'XXX' is the iteration for generate map
    """

    def __init__(self, genData, listMetadataToCreate):
        super(GeneratorMap, self).__init__()
        self.imgDestination = genData.storagePath.text()
        self.fileName = genData.mapName.text()
        self.imgFormat = genData.extension.currentText()
        self.composerName = genData.composer.composerWindow().windowTitle()
        self.taxonList = genData.taxonList
        self.whereEditable = genData.whereEditable.text()
        self.fieldName = genData.iterationField.currentText()
        self.layerName = genData.layer.name()
        self.projectName = genData.projectName.currentText()

        self.create_json_project_qgis()

        self.composer = genData.composer.composition()
        self.layer = genData.layer
        self.projectXML = listMetadataToCreate

        self.timerInit(len(self.taxonList))

        #Creation of the csv file which will contains all the taxon generate
        path = self.imgDestination+'/'+self.fileName+'.csv'
        try:
            with open(path, 'wb') as csvfile:
                #Csv is delimited by ";"
                writer = csv.writer(csvfile, delimiter=';')
                #Write each taxon with their description
                writer.writerows([(filter(lambda x: x != "'", unicode(taxon[0]).encode("utf-8")),unicode(taxon[1]).encode("utf-8")) for taxon in self.taxonList])
        except Exception as e:
            self.logProgress.emit(Logger.ERROR, u"Génération du fichier csv impossible")
            
    def create_json_project_qgis(self):
        """
            This method represent a json file resulting of the process generation
        """
        try:
            #Create a json file which represent what append during the generation
            genDataJSON = self.to_JSON()
            metaWriter = MetadataWriter("generation_info_"+str(time.strftime("%Y%m%d%H%M%S")), self.imgDestination, genDataJSON)
            metaWriter.process()
        except Exception as e:
            self.logProgress.emit(Logger.ERROR, u"Génération du fichier generation_info.json impossible")

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def getResult(self):
        return None

    def run(self):
        """
        This method is the algorithme of generation map
        """
        try:
            #Start the log
            self.logProgress.emit(Logger.INFO, u"=> Début de la génération <=")
            #Get the number of map to generate
            nbTaxon = len(self.taxonList)

            self.logProgress.emit(Logger.INFO, u"Projet : " + str(self.projectName))
            self.logProgress.emit(Logger.INFO, u"Nom de carte : " + str(self.fileName) + u"_[cd_ref]." + self.imgFormat)
            self.logProgress.emit(Logger.INFO, u"Nombre d'images à générer : " + str(nbTaxon))

            if self.whereEditable != '':
                self.whereEditable = " AND " + self.whereEditable


            for taxon in self.taxonList:
                self.timerNewTurn()
                self.timerNotify()

                if(self.isKilled() == True):
                    break
                self.logProgress.emit(Logger.INFO, str(taxon) + u" : En cours de génération")

                #Map generation--------------------------------------------------------------------------------
                #Remove '' from the taxon's string
                nameTaxon = filter(lambda x: x != "'", taxon[0])
                #Create the filename of the map
                self.file_name = str(self.fileName)+ "_" + nameTaxon + "." + self.imgFormat
                #Create the layer filter
                filterLayer = self.fieldName +" = "+ taxon[0] + self.whereEditable
                self.logProgress.emit(Logger.INFO, str(taxon) + u" : Filtre appliqué : " + filterLayer)

                if(self.isKilled() == True):
                    break
                try:
                    # Apply the filter
                    result = QgisUtils.set_subsetstring(self.layer, filterLayer)
                    if(self.isKilled() == True):
                        break
                    if result == False:
                        raise GenerateException(u"Conditions de filtrages incorectes : " + filterLayer)
                    # Generate the map
                    image = QgisUtils.composer_printPageAsRaster(self.composer)
                    if(self.isKilled() == True):
                        break
                    if image is None:
                        raise GenerateException(u"Erreur récupération du composer")
                    # Save the map in the system file
                    result = QgisUtils.composer_saveImage(image, self.imgDestination + "/" + self.file_name, self.imgFormat)
                    if(self.isKilled() == True):
                        break
                    if result == False:
                        raise GenerateException(u"Erreur enregistrement carte")
                except GenerateException as e:
                    self.logProgress.emit(Logger.ERROR, str(taxon) + " : " + str(e))
                    continue
                except Exception as e:
                    self.logProgress.emit(Logger.ERROR, str(taxon) + u" : Erreur globale de génération : " + str(e))
                    continue
                self.logProgress.emit(Logger.INFO, str(taxon) + u" : Génération IMG OK")
                if(self.isKilled() == True):
                    break
                # metadata -------------------------------------------------------------------------------------------
                try:
                    #Create the json structure
                    metadata = self.populate_json_object(taxon[0],taxon[1])
                    if(self.isKilled() == True):
                        break
                    #Create the json file 
                    metaWriter = MetadataWriter(self.file_name, self.imgDestination, metadata.to_JSON())
                    if(self.isKilled() == True):
                        break
                    #Run the process metadata writing
                    metaWriter.process()
                    if(self.isKilled() == True):
                        break
                except Exception as e:
                    self.logProgress.emit(Logger.ERROR, str(taxon) + u" : Erreur génération Metadata " + str(e))
                    continue
                self.logProgress.emit(Logger.INFO, str(taxon) + u" : Génération Metadata OK")
                if(self.isKilled() == True):
                    break

            self.timerEnd()
        except Exception as e:
            self.logProgress.emit(Logger.ERROR, u"Erreur lors de la génération : " + str(e))
            pass
        self.logProgress.emit(Logger.INFO, u"=> Génération terminée <=")

    def get_value_from_metadata(self, value):
        """
            This method get the value of metadata according to the param
            :returns: value of the metadata
        """
        #Get the value of each metadata
        for item, v in enumerate(self.projectXML):
            if v[0] == value:
                return v[1]

    def populate_json_object(self, taxon, description):
        """
            Create a json structure with all metadata
            :returns metadata: represent the json with all metadata
        """
        metadata = ObjectJSON()
        metadata.generationDate = str(time.strftime("%Y-%m-%d"))
        metadata.dpi = str(QgisUtils.composer_printResolution(self.composer))
        metadata.extension = str(self.imgFormat)
        metadata.dimension = str(QgisUtils.composer_height(self.composer)) + "," + str(QgisUtils.composer_width(self.composer))
        statinfo = os.stat(self.imgDestination + "/" + self.file_name)
        metadata.weight = str(statinfo.st_size/1024)
        
        maps = QgisUtils.composer_MapItems(self.composer)
        myMap = None
        area = 0
        # Get the largest map from a composer and get his extent
        for mapItem in maps:
            value = QgisUtils.mapItem_boundingRect_width(mapItem) * QgisUtils.boundingRect_height(mapItem)
            if area < value:
                myMap = mapItem
                area = value

        metadata.bbox = []
        metadata.bbox.append(QgisUtils.currentMapExtent_xMinimum(myMap))
        metadata.bbox.append(QgisUtils.currentMapExtent_yMinimum(myMap))
        metadata.bbox.append(QgisUtils.currentMapExtent_xMaximum(myMap))
        metadata.bbox.append(QgisUtils.currentMapExtent_yMaximum(myMap))
        metadata.projection = str(QgisUtils.layer_crs_authid(self.layer))
        metadata.taxon = ObjectJSON()

        metadata.taxon.cdref = taxon
        metadata.taxon.name = description
        metadata.organizationCbn = self.get_value_from_metadata("cbnOrganisation")
        metadata.email = self.get_value_from_metadata("contactEmail")
        metadata.projectDescription = self.get_value_from_metadata("description")
        metadata.projectName = self.get_value_from_metadata("projectName")
        metadata.rangeObservationStart = self.get_value_from_metadata("studyStartDate")
        metadata.rangeObservationEnd = self.get_value_from_metadata("studyEndDate")
        metadata.dataOwner = self.get_value_from_metadata("dataOwner")
        metadata.projectModificationDate = self.get_value_from_metadata("dateModification")
        metadata.versionNumber = self.get_value_from_metadata("projectVersion")
        metadata.genealogyData = self.get_value_from_metadata("genealogyData")
        metadata.thesaurusISO = self.get_value_from_metadata("thesaurusISO")
        metadata.thesaurusINSPIRE = self.get_value_from_metadata("thesaurusInspire")
        metadata.keywords = []
        metadata.keywords = [val.strip() for val in self.get_value_from_metadata("keywords").split(',')]
        metadata.contact = self.get_value_from_metadata("contact")
        metadata.cbnManager = self.get_value_from_metadata("cbnManager")
        metadata.updateFrequency = self.get_value_from_metadata("updateFrequency")
        metadata.usageLimit = self.get_value_from_metadata("usageLimit")
        metadata.dataState = self.get_value_from_metadata("dataState")

        return metadata


    
