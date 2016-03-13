# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plantmap_progress_base.ui'
#
# Created: Wed Feb 24 16:51:57 2016
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PlantMapDialogBase(object):
    def setupUi(self, PlantMapDialogBase):
        PlantMapDialogBase.setObjectName(_fromUtf8("PlantMapDialogBase"))
        PlantMapDialogBase.resize(452, 295)
        PlantMapDialogBase.setMaximumSize(QtCore.QSize(16777215, 1400))
        self.verticalLayout = QtGui.QVBoxLayout(PlantMapDialogBase)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(PlantMapDialogBase)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.UI_log = QtGui.QTextEdit(PlantMapDialogBase)
        self.UI_log.setObjectName(_fromUtf8("UI_log"))
        self.verticalLayout.addWidget(self.UI_log)
        self.UI_progressBar = QtGui.QProgressBar(PlantMapDialogBase)
        self.UI_progressBar.setProperty("value", 0)
        self.UI_progressBar.setObjectName(_fromUtf8("UI_progressBar"))
        self.verticalLayout.addWidget(self.UI_progressBar)
        self.UI_Cancel = QtGui.QPushButton(PlantMapDialogBase)
        self.UI_Cancel.setObjectName(_fromUtf8("UI_Cancel"))
        self.verticalLayout.addWidget(self.UI_Cancel)

        self.retranslateUi(PlantMapDialogBase)
        QtCore.QMetaObject.connectSlotsByName(PlantMapDialogBase)

    def retranslateUi(self, PlantMapDialogBase):
        PlantMapDialogBase.setWindowTitle(QtGui.QApplication.translate("PlantMapDialogBase", "PlantMap : Map Generator", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PlantMapDialogBase", "Retrouvez tous les logs dans le fichier log.txt", None, QtGui.QApplication.UnicodeUTF8))
        self.UI_Cancel.setText(QtGui.QApplication.translate("PlantMapDialogBase", "Fermer", None, QtGui.QApplication.UnicodeUTF8))

