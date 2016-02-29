# coding: utf8

from plantmap_engine import plantMapEngine
from qgis_utils import QgisUtils

class externalProcessThreadInterface:
	"""
		This class simulate an interface which represent a treatment before and after the launch of the thread
	"""
	def before(self):
		pass

	def after(self, result):
		pass


class loadCSVExternalProcess(externalProcessThreadInterface):
	"""
		This class represent the treatment before and after the thread launch which load a CSV in the taxon board
	"""
	def __init__(self):
		self.taxonList = []

	def before(self):
		"""
			Nothing to do before
		"""
		pass

	def after(self, result):
		"""
			Get the list of taxon from the loading 
		"""
		self.taxonList = result


class deepExternalProcessValidation(externalProcessThreadInterface):
	"""
		This class represent the treatment before and after the thread launch which make a deep search in the layer
	"""

	def __init__(self, layer):
		self.oldSubSet = ""
		self.layer = None
		self.taxonList = None
		self.layer = layer
		self.pme = plantMapEngine()

	def before(self):
		"""
			Get the current subset filter before the treatment
		"""
		self.oldSubSet = QgisUtils.get_subsetstring(self.layer)

	def after(self, result):
		"""
			Replace the subset filter with the user's one and get the list of taxon returned by the thread
		"""
		QgisUtils.set_subsetstring(self.layer, self.oldSubSet)
		self.taxonList = result


class generatorMapExternalProcess(externalProcessThreadInterface):
	"""
		This class represent the treatment before and after the thread launch of the map generation
	"""

	def __init__(self, layer):
		self.oldSubSet = ""
		self.layer = None
		self.layer = layer


	def before(self):
		"""
			Get the current subset filter before the thread
		"""
		self.oldSubSet = QgisUtils.get_subsetstring(self.layer)

	def after(self, result):
		"""
			Replace the subset filter with the previous one
		"""
		QgisUtils.set_subsetstring(self.layer, self.oldSubSet)

