# coding: utf8

from PyQt4 import QtGui
import codecs
import threading
from logger import *

class HandlerInterface(QObject):
	"""
		This class simulate an interface for the logger which allow him to be threadsafe
	"""
	def close(self):
		pass
	def emit(self,record):
		pass

class FileHandler(HandlerInterface):
	"""
		This class implement the interface HandlerInterface to log informations in a file
	"""

	def __init__(self, pathFile):
		super(FileHandler,self).__init__()
		self.fileLog = None
		self.lock = threading.Lock()
		with self.lock:
			if self.fileLog is None:
				self.fileLog = codecs.open(pathFile, "a", "utf-8")

	def close(self):
		"""
			Close the file log
		"""
		with self.lock:
			if self.fileLog is not None:
				self.fileLog.close()

	def emit(self, level, mess):
		"""
			Send a message to write in the file
		"""
		with self.lock:
			if self.fileLog is not None:
				self.fileLog.write(mess)
				self.fileLog.write(u"\n")


class TextEditHandler(HandlerInterface): 
	"""
		This class implement the interface HandlerInterface to log informations in the console and tab lineedit
	"""
	def __init__(self, UI_log):
		super(TextEditHandler,self).__init__()
		self.UI_logViewPlugin = UI_log

	def emit(self, level, mess):
		"""
			Send a message to write in each display with a color
		"""
		try:
			if level == Logger.DEBUG:
				self.UI_logViewPlugin.setTextColor(QtGui.QColor('green'))
			if level == Logger.INFO:
				self.UI_logViewPlugin.setTextColor(QtGui.QColor('blue'))
			if level == Logger.ERROR:
				self.UI_logViewPlugin.setTextColor(QtGui.QColor('red'))
			self.UI_logViewPlugin.append(mess)
		except:
			pass

	def close(self):
		"""
			Close the dialog
		"""
		pass
