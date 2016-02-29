# coding: utf8

import os
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox
from logger import *
from handlers import *
import plantmap_progress_base

class PlantMapProgress(QtGui.QDialog, plantmap_progress_base.Ui_PlantMapDialogBase):
	"""
	This class is a modal for the plugin.
	This modal block Qgis and plugin for execute a long task in a thread
	"""

	logSignal = QtCore.pyqtSignal(int)
	def __init__(self,threadProcess, threadExternalProcess, pathFileLog=None):
		QtGui.QDialog.__init__(self)
		self.setupUi(self)
		#Link the Cancel bouton
		self.UI_Cancel.clicked.connect(self.close)
		self.threadProcess = threadProcess
		self.externalProcess = threadExternalProcess
		#Link 2 signal between the thread and the main thread.
		#notifyProgress signal is used for move the progress bar (get 2 int arguements)
		self.threadProcess.notifyProgress.connect(self.setProgressBar)
		#logProgress signal is used for the log. The thread is not allowed to change the UI directly
		self.threadProcess.logProgress.connect(self.postLog)
		#Get the logger and added the EditText 
		self.logger = Logger()
		self.handler = TextEditHandler(self.UI_log)
		self.logger.addOutput(self.handler)
		# added a file for write the log (if a path was passed)		
		self.fileHandler = None
		if pathFileLog is not None:
			self.fileHandler = FileHandler()
			self.fileHandler.open(pathFileLog + "/log.txt")
			self.logger.addOutput(self.fileHandler) 

		#In this function, you can excecute actions, in Main thread juste beore sart the thread
		#Check IexternalProcessThread.py and implement externalProcessThreadInterface
		self.externalProcess.before()
		#Stared the thread. Normally, we should used "movetothread" method I think
		self.threadProcess.start()



	def postLog(self, level, mess):
		"""
		The thread was link with this method for log every information.
		Level is a Logger.[DEBUG|INFO|ERROR]
		mess is a unicode
		"""
		mess = mess.encode('utf-8')
		if level == Logger.DEBUG:
			self.logger.debug(mess)
		if level == Logger.INFO:
			self.logger.info(mess)
		if level == Logger.ERROR:
			self.logger.error(mess)


	def setProgressBar(self, time, percent):
		"""
		The thread was link with this method for incremente the progress Bar on the modal
		time is a int. Represente the remaining time in seconds before the end of process
		percent is a int. Represente the percent of completion process
		"""
		#if time is negative, the time isn't calculate
		if time < 0 :
			self.UI_progressBar.setFormat("Temps restant : < Calcul en cours >         " + str(percent) + " %")
			return
		#transforme the second on string understandable 
		hours = time / 60 / 60 % 24
		minutes = time / 60 % 60
		seconds = time % 60
		timeTreat = ""
		if hours > 0:
			timeTreat = str(hours) + " H "
		if minutes > 0:
			timeTreat += str(minutes) + " min "
		timeTreat += str(seconds) + " sec."
		
		#And change value of progressbar
		self.UI_progressBar.setFormat("Temps restant : " + timeTreat + "          " + str(percent) + " %")
		self.UI_progressBar.setValue(percent)

		if(percent==100):
			QMessageBox.information(self,
			self.trUtf8("Processus"),
			self.trUtf8("Processus terminée"))


	def closeEvent(self,event):
		"""
		This method was call when the user click on "Cancel" bouton
		If the thread isn't finish, we propose to wait the end of process or to kill the thread.
		"""
		if self.threadProcess.isRunning() == True:
			reply = QtGui.QMessageBox.question(self,'Message',u"Le traitement n'est pas terminé\nSouhaitez-vous l'arrêter ?",QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
			#if we want kill the thread
			if reply == QtGui.QMessageBox.Yes:
				self.logger.info("Arrêt du traitement en cours")
				self.end(event)
			else:
				event.ignore()
		else:
			self.end(event)

	def end(self, event):
		"""
		This method is always call after close the modal.
		this method check if the thread if finish and remove TextEditHandler and fileHandler
		"""
		self.threadProcess.kill()
		self.threadProcess.quit()
		self.threadProcess.wait()
		self.threadProcess.deleteLater()
		self.logger.removeOutput(self.handler)
		if self.fileHandler is not None:
			self.logger.removeOutput(self.fileHandler)
		#Like the "before" method, "after" method was called by th main Thread at the end of thread process
		#Check IexternalProcessThread.py and implement externalProcessThreadInterface
		self.externalProcess.after(self.threadProcess.getResult())
		event.accept()

