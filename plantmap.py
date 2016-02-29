# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PlantMap
                                 A QGIS plugin
 This plugin provide a genertor of multitude maps
                              -------------------
        begin                : 2015-11-23
        git sha              : $Format:%H$
        copyright            : (C) 2015 by GreenMapper
        email                : maxencebunel77@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog

from plantmap_dialog import PlantMapDialog
import os.path
import logging
from logger import *
from handlers import *

class PlantMap:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        if not os.path.exists(self.plugin_dir+'/project'):
            os.mkdir(self.plugin_dir+"/project/")
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PlantMap_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = PlantMapDialog(self.iface)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&PlantMap : Map Generator')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PlantMap')
        self.toolbar.setObjectName(u'PlantMap')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PlantMap', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/PlantMap/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # slots/signals
        ###############
        self.initDone = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&PlantMap : Map Generator'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        #Load the field QComboBox [Layer, fieldLayer, Composer, ...]

        self.dlg.UI_linkExpression.setText('''<a href='https://docs.qgis.org/2.8/en/docs/user_manual/working_with_vector/expression.html'>(Qgis Doc)</a>''')
        self.dlg.UI_linkExpression.setOpenExternalLinks(True)

        self.set_layers_list() # Add the layer list
        self.set_field_description_layer() # add the field of selected layer
        self.dlg.UI_taxonLayer.currentIndexChanged.connect(self.set_field_description_layer) # Run function if item in qComboBox is selected (This is a signal)
        self.set_composer_list()
        self.dlg.select_project(self.dlg.UI_projectSelection)
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    """
    The next method init all the QComboBox in the UI generateMap
    """
    def set_layers_list(self):
        """
        this method add all current names of layers and the layers objects in a qComboBox.
        The qComboBox is pass in argument
        """
        self.dlg.UI_taxonLayer.clear()
        [self.dlg.UI_taxonLayer.addItem(layer.name(), layer) for layer in self.iface.legendInterface().layers()]

    def set_field_description_layer(self):
        """
        This method add the field of the selected layer in a qComboBox
        We cannot pass an another argument, this method is a signal.
        """
        self.dlg.UI_iterationField.clear() # Clean the items of the qComboBox
        self.dlg.UI_descriptionField.clear() # Clean the items of the qComboBox
        layer_selected = self.dlg.UI_taxonLayer.itemData(self.dlg.UI_taxonLayer.currentIndex()) # Get the object layer in the qComboBox
        if(layer_selected != None):
            self.dlg.UI_iterationField.addItems([field.name() for field in layer_selected.pendingFields()]) #Added all the field.
            self.dlg.UI_descriptionField.addItems([field.name() for field in layer_selected.pendingFields()]) #Added all the field.

    def set_composer_list(self):
        """
        This method add the composer in a qCombox
        The qComboBox is pass in argument
        """
        self.dlg.UI_composerName.clear()
        for composer in self.iface.activeComposers():
            self.dlg.UI_composerName.addItem(composer.composerWindow().windowTitle(), composer)

   

    """
    End of init qComboBox for UI generateMap
    """
