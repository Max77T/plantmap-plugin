# coding: utf8

import time
from PyQt4.QtCore import QObject
from PyQt4 import QtCore
import threading

lock = threading.Lock()

class Logger(QObject):
	"""
	This class Logger propose to log with 3 level for 3 output
	Level : DEBUG | INFO | ERROR

	The Logger used handlers. You can create handlers and added this with class Handlers
	"""

	DEBUG = "DEBUG"
	INFO = "INFO"
	ERROR = "ERROR"

	outputList = []
	instance = None

	def __new__(cls):
		with lock:
			if cls.instance is None:
				cls.instance = QObject.__new__(cls)
				cls.instance.outputList = []
			return cls.instance

	def __init__(self):
		with lock:
			super(Logger, self).__init__()

	def addOutput(self, outputBranch):
		with lock:
			self.outputList.append(outputBranch)

	def removeOutput(self, outputBranch):
		with lock:
			for i, o in enumerate(self.outputList):
			    if o == outputBranch:
			    	outputBranch.close()
			        del self.outputList[i]
			        break
	"""
	LEVEL
	"""
	def debug(self, mess):
		"""
			This method display a green message which is usefull to the developper
		"""
		try:
			newMess = unicode(str(time.strftime("%Y-%m-%d %H:%M:%S")) + " ::DEBUG:: {m}".format(m=mess), "utf-8")
		except UnicodeError:
			newMess = mess.encode('utf-8')
		for out in self.outputList:
			out.emit(Logger.DEBUG, newMess)

	def info(self, mess):
		"""
			This method display a blue message which indicate to the user the progress of the operation
		"""
		try:
			newMess = unicode(str(time.strftime("%Y-%m-%d %H:%M:%S")) + " ::INFO:: {m}".format(m=mess), "utf-8")
		except UnicodeError:
			newMess = mess.encode('utf-8')
		for out in self.outputList:
			out.emit(Logger.INFO, newMess)

	def error(self, mess):
		"""
			This method display a red message which show an Error during the process
		"""
		try:
			newMess = unicode(str(time.strftime("%Y-%m-%d %H:%M:%S")) + " ::ERROR:: {m}".format(m=mess), "utf-8")
		except UnicodeError:
			newMess = mess.encode('utf-8')
		for out in self.outputList:
			out.emit(Logger.ERROR, newMess)
