# coding: utf8

from PyQt4.QtCore import QThread, pyqtSignal

from timer import *

class PlantMapThreadInterface(QThread):
	"""
		This class simulate an interface that a thread need to implement
	"""
	def run(self):
		"""
			Represent the main work of the thread
			TODO : Need to implement this method
		"""
		pass

	def getResult(self):
		"""
			Allow PlantMap to get the result of the thread
			TODO : Need to implement this method
		"""
		pass


	killed = False
	timer = None

	notifyProgress = pyqtSignal(int, int)
	logProgress = pyqtSignal(str, str)

	def isKilled(self):
		"""
			Return the status of the thread isalive or not
			:returns: True if the thread is dead or False if not
		"""
		return self.killed

	def kill(self):
		"""
			Kill a thread
		"""
		self.killed = True


	def timerInit(self, nbTotal):
		"""
			Initialize the timer of the thread
			:param nbTotal: represent the number of entities that the thread has to process
		"""
		self.timer = Timer(nbTotal)

	def timerNotify(self):
		"""
			Notify the thread to the time spend and the percent
		"""
		self.notifyProgress.emit(round(self.timer.computeTimeProgress()), round(self.timer.computePercentProgress()))

	def timerEnd(self):
		"""
			Represent the end of the timer
		"""
		self.notifyProgress.emit(0, 100)

	def timerNewTurn(self):
		"""
			Update the display time and percent
		"""
		self.timer.newTurn()
