# coding: utf8



class Project:
	"""
		This class represents a project of the plugin
	"""

	def __init__(self,
		name, 
		description,
		contactName,
		contactEmail,
		cbnOrganisation,
		studyStartDate,
		studyEndDate,
		projectVersion,
		thesaurusISO,
		thesaurusInspire,
		keywords,
		contact,
		dataOwner,
		genealogyData,
		cbnManager,
		updateFrequency,
		usageLimitation,
		dataState,
		dateModification):

		self.name = name # Name of the project 
		self.description = description # Description of the project
		self.contactName = contactName # Name of the contact of the project
		self.contactEmail = contactEmail # Email of the contact
		self.cbnOrganisation = cbnOrganisation # CBN 
		self.studyStartDate = studyStartDate # Start date
		self.studyEndDate = studyEndDate # End date
		self.projectVersion = projectVersion # Version of the project
		self.thesaurusISO = thesaurusISO
		self.thesaurusInspire = thesaurusInspire
		self.keywords = keywords # List of keywords
		self.contact = contact
		self.dataOwner = dataOwner
		self.genealogyData= genealogyData
		self.cbnManager = cbnManager
		self.updateFrequency = updateFrequency
		self.usageLimitation = usageLimitation
		self.dataState = dataState
		self.dateModification = dateModification
