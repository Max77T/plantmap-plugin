# coding: utf8

from xml import etree
from xml.etree import ElementTree
from xml.dom import minidom
import unicodedata
import codecs
import os
import xml.etree.ElementTree as ET

class plantMapXML:

	def xml_writer(self,project):
		"""
			This method will create a xml file which contains all the metadata from a project
		"""
		projectData = [
		("projectName",project.name),
		("description",project.description),
		("contactName",project.contactName),
		("contactEmail",project.contactEmail),
		("cbnOrganisation",project.cbnOrganisation),
		("studyStartDate", project.studyStartDate.toString('yyyy-MM-dd')),
		("studyEndDate",project.studyEndDate.toString('yyyy-MM-dd')),
		("projectVersion",project.projectVersion),
		("dateModification",project.dateModification)
		]

		metadatas = [
		("thesaurusISO",project.thesaurusISO),
		("thesaurusInspire",project.thesaurusInspire),
		("contactInspire",project.contactInspire),
		("dataOwner",project.dataOwner),
		("genealogyData",project.genealogyData),
		("cbnManager",project.cbnManager),
		("updateFrequency",project.updateFrequency),
		("usageLimit",project.usageLimitation),
		("dataState",project.dataState)
		]

		keywords = project.keywords
		
		projectXML = ET.Element("project")

		# Put the data project into the xml tree
		for data in projectData:
			proj = ET.SubElement(projectXML,data[0])
			proj.text = data[1]
		
		# Put metadatas of the project into the xml tree
		for meta in metadatas:
			metas = ET.SubElement(projectXML,meta[0])
			metas.text = meta[1]

		# Put keywords into the xml tree
		word = ET.SubElement(projectXML,"keywords")
		for keyword in keywords:
			w = ET.SubElement(word, "word")
			w.text=keyword

		# Path of output file
		path = os.path.dirname(__file__)
		outfile = codecs.open(path+"/project/"+ unicode(project.name).encode("utf-8") +".xml",'w',"utf-8")

		tree = self.prettify(projectXML)	
		#Writing of the xml file
		outfile.write(unicode(tree))  
		#Closing file
		outfile.close()

	def parse_xml(self,fileName):
		tree = ET.parse(fileName)
		root = tree.getroot()
		return root			

	def prettify(self, elem):
	    """
	    	Return a pretty-printed XML string for the Element.
	    	:returns: pretty xml
	    """
	    rough_string = ElementTree.tostring(elem, 'utf-8')
	    reparsed = minidom.parseString(rough_string)
	    return reparsed.toprettyxml(indent="  ")