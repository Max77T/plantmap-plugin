# coding: utf8

import json
import os

class MetadataWriter:

	def __init__(self, fileName, path, json):
		self.storagePath = path
		self.fileName = fileName
		self.jsonMetadata = json

	def process(self):
		"""
			This method create the directory of metadata and create for each map a metadata file
		"""
		self.create_dir_metadata()
		self.write()

	def create_dir_metadata(self):
		"""
			Create a metadata project if is not present in the directory of the map generation
		"""
		newpath = self.storagePath + "/metadata"
		#Create the metadata's directory if it's not exist
		if not os.path.exists(newpath):
			os.makedirs(newpath)

	def write(self):
		with open(self.storagePath + "/metadata/"+ self.fileName +".json", mode="wb+") as outfile:
			outfile.write(self.jsonMetadata)


