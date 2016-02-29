# coding: utf8

from __future__ import division
from datetime import datetime

class Timer:
	"""
	This class calculate the time and the percent for finish a process
	"""
	def __init__(self, nbProcess):
		self.leftTaxon = nbProcess
		self.totalTaxon = nbProcess
		self.treatTaxon = 0
		self.totalTime = 0
		self.startTime = 0
		self.endTime = None

	def newTurn(self):
		"""
		You need to call this method for change the state of the class
		After that, you can call the differents methods
		"""
		if self.endTime is None:
			self.endTime = datetime.now()
			return

		self.startTime = self.endTime
		self.endTime = datetime.now()

		actualTime = self.endTime - self.startTime # !! Carfuly : The time is inversed !!
		self.totalTime = self.totalTime + actualTime.total_seconds()
		self.leftTaxon -= 1
		self.treatTaxon += 1

	def computeTimeProgress(self):
		"""
		return -1 if the time is in progress to calculate (infinite)
		else, return the total time for finish the process
		"""
		if self.treatTaxon == 0 :
			return -1
		leftOverTime = (self.totalTime / self.treatTaxon) * self.leftTaxon
		return leftOverTime



	def computePercentProgress(self):
		"""
		Return the percent already done
		"""
		if self.totalTaxon == 0 :
			return -1
		percentLeft = 100 / self.totalTaxon * self.treatTaxon
		return percentLeft

