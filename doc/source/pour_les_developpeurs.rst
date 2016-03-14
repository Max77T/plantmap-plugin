========================
Pour les développeurs
========================
Ce document a pour objectif de décrire les différents outils et API nécessaire à la poursuite du développement du plugin QGIS. Il permettra, dans une perspective d’évolution, de reprendre le développement dans un environnement similaire à celui que nous avons installé. Cette documentation relatera dans une première partie les outils indispensables à la poursuite du développement et dans une seconde partie l’organisation du code.

---------------------------------
L'environnement de développement
---------------------------------
Les outils présentés permettront de développer de nouvelles fonctionnalités et de mettre à jour l’application si nécessaire (QGIS 3.0 par exemple)

^^^^^^^
QGIS
^^^^^^^
L’outil développé par l’équipe s’appuie sur la suite logicielle QGIS, logiciel de type SIG, open source et gratuit. Le cœur du logiciel a été développé principalement à l’aide de C++ et offre une API utilisable en langage python et C++.

Installation : https://www.qgis.org/fr/site/forusers/alldownloads.html#debian-ubuntu

Si la version de python n’est pas à jour ou n’est pas installé : apt-get install python-qgis

Pour les novices dans le développement de plugin QGIS, les ressources suivantes peuvent être itnéressantes :
  * http://plugins.qgis.org/
  * http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/plugins.html

^^^^^^^^^^^^^^
Qtcreator
^^^^^^^^^^^^^^
QtCreator est un IDE qui permet de réaliser des applications multiplateformes. De ce fait, l’outil QtDesigner de la suite logiciel permet à l’aide d’un système de drag&drop de créer des interfaces utilisateurs de manière simple. Ces interfaces sont réalisées en XML et transformables en fichier interprétable par python (PyQT). Par ailleurs, c’est cette technologie qui est utilisée par QGIS lui-même pour designer ses interfaces.

Installation : http://www.qt.io/download/

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SublimeText
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Nous conseillons d’utiliser SublimeText un éditeur OpenSource reconnaissant python avec coloration syntaxique. Cependant il est toujours possible d’utiliser des IDE plus sophistiqué tels qu’Eclipse ou PyCharm.

Installation: https://www.sublimetext.com/3

^^^^^^^^^^
Sphinx 
^^^^^^^^^^
Cette documentation a été produite grâce au générateur de documentation Python Sphinx

Installation : http://www.sphinx-doc.org/

Pour les novices de Sphinx, les ressources suivantes peuvent être intéressantes :
  * http://www.sphinx-doc.org/en/stable/tutorial.html#adding-content
  * http://www.sphinx-doc.org/en/stable/rest.html#rst-primer
  * http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#simple-tables

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Plugin Reloader (plugin QGIS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Cet outil est indispensable si une mise à jour du plugin est prévue. En effet, cet outil est un plugin QGIS qui permet de recompiler le code et de relancer l’application de manière simple et efficace. 

Installation :

  * Ouvrir QGIS
  * Se rendre dans le menu “Extention -> Installer/Gérer les extensions”
  * Rechercher “plugin reloader”
  * Installer

Ensuite, lors d’un changement dans le code du plugin, il suffit de sélectionner le plugin modifié en cliquant sur l’icône du plugin reloader.

---------------------------------
Organisation générale du plugin
---------------------------------

^^^^^^^^^^^^^^^^^^^^^^^^^
Les différents dossiers
^^^^^^^^^^^^^^^^^^^^^^^^^
Le dossier comportant le code du plugin rassemble toutes les fonctions, classes et méthodes à la racine du dossier.
Le dossier présente plusieurs dossiers :

=======   ============
Dossier   Description
=======   ============
i18n      fichiers pour l'internationalisation du plugin (anglais, français)
img       images utilisées dans la documentation
project   fichiers XML décrivant les projets définis dans le plugin
scripts   quelques scripts shell divers 
test      tests unitaires
=======   ============

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Les fichiers de développement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Ces fichiers sont utilisé majoritairement dans le cadre du développement du plugin

================  ===================
Fichier           Description
================  ===================
.travis.yml        YML utilisé pour faire les test unitaires (https://docs.travis-ci.com/)
Makefile          Fichier facilitant la gestion de la compilation du pugin
pb_tool.cfg.txt   Configuration file for plugin builder tool (pb_tool)
plugin_upload.py  This script uploads a plugin package on the server
pylintrc          Pylint is a tool that checks for errors in Python code
qgis_utils.py     contient les fonctions qgis utilisées à travers le plugin afin de faciliter au mieux un changement de version. Certaines fonctions QGIS peuvent néanmoins se trouver dans certains fichiers.
================  ===================

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Les interfaces
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Ces fichiers sont constitues les 

==========================   ======================================================================================================================    ====================================================================================================================
Fichier                      Description                                                                                                               Classes et méthodes
==========================   ======================================================================================================================    ====================================================================================================================
handlers.py                  permet de gerer le lien entre l'interface et les logs                                                                     HandlerInterface(close, emit), FileHandler(__init__, close, emit), TextEditHandler (__init__, close, emit)
plantmap.py                  QGIS Plugin Implementation : initialise les composants de l’interface graphique avec les informations du projet QGIS      PlantMap (__init__, tr, add_action, initGui, unload, run, set_layers_list, set_field_description_layer, set_composer_list)
plantmap_dialog.py           instancie et fait le lien avec plantmap_dialog_base.py                                                                    PlantMapDialog(__init__,next, prev, next2, prev2, check_where_editable, check_state_map_name, check_state_date, check_state, check_state_description, check_state_email, check_state_project_name, put_to_false, deep_validation, stockage_file_dialog, taxon_list_file_dialog, export_file_dialog, export, select_project, set_project_selection_combobox, test_sender, valide_select_project, get_project_from_xml, validate_project_creation, fill_project_field, fill_project_tab, validate_export, validate_taxon, validate_remove_all, validate_map_generation, new_add_taxon_to_board, refresh_taxon_board, check_type, check_isString, error_message, en_of_generate, generate)
plantmap_dialog_base.py      compilation plantmap_dialog_base.ui (pyuic4)                                                                              Ui_PlantMapDialogBase
plantmap_dialog_base.ui      XML : interface générale du plugin issu de QTCreator                                                                      ..
plantmap_progress.py         instancie et gère plantmap_progress_base.py. This class is a modal for the plugin.                                        This modal block Qgis and plugin for execute a long task in a thread	PlantMapProgress(__init__, postLog, setProgressBar, closeEvent, end)
plantmap_progress_base.py    compilation plantmap_progress_base.ui (pyuic4)                                                                            Ui_PlantMapDialogBase
plantmap_progress_base.ui    XML : interface de la modal issu de QTCreator                                                                             ..
==========================   ======================================================================================================================    ====================================================================================================================

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Les différentes classes et méthodes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Ces fichiers sont constitues le coeur du plugin.

==========================   ============================================================================================================================================   ====================================================================================================================
Fichier                      Description                                                                                                                                    Classes et méthodes
==========================   ============================================================================================================================================   ====================================================================================================================
__init__.py                  This script initializes the plugin,  making it known to QGIS.                                                                                  Def classFactory
deepValidationProcess.py     permet de vérifier la présence d'un taxon dans les données sources (modifie le statut de présence).                                            deepValidation (__init__,  run,  getResult)
export.py                    permet de créer un zip avec les cartes et les métadonnées                                                                                      Export(__init__, process, fill_list_of_img, fill_list_of_metadata, intersect_list_image_metadata, createZip)
generationData.py            constructeur des paramètres de production de la carte (metadata of a generation)                                                               generationData(__init__)
IexternalProcessThread.py    permet de gerer le lien entre le pré et post traitement lors des actions d'import de CSV,  de recherche avancée et de production de cartes     externalProcessThreadInterface(before, after),  loadCSVExternalProcess (__init__, before, after),  deepExternalProcessValidation(__init__, before, after),  generatorMapExternalProcess(__init__, before, after)
IplantMapThread.py           This class simulate an interface that a thread need to implement                                                                               PlantMapThreadInterface
loadCSVProcess.py            permet de charger une liste de taxon                                                                                                           loadCSV(__init__, run, getResult)
Logger.py                    This class Logger propose to log with 3 level for 3 output Level : DEBUG | INFO | ERROR
                             The Logger used handlers. You can create handlers and added this with class Handlers                                                           Logger(__new__, __init__, addOutput, removeOutput, debug, info, error)
manageUIListTaxon.py         Manage all the taxon in the UI list and in the list for generation. This class is an singleton,  
                             but the singleton fonctionnalities are not used for the moment.                                                                                ManageUIListTaxon(__new__, __init__, initManager, getListOfTaxon, addTaxon, refreshTaxonTab, removeAll, handler_remove_button)
mapgenerator.py              lance la génération des toutes les cartes                                                                                                      GeneratorMap(__init__, create_json_project_qgis, to_JSON, getResult, run, get_value_from_metadata, populate_json_object)
metadata_writer.py           Créer les métadonnées des cartes                                                                                                               MeadataWriter(__init__, process, create_dir_metadata, write)
plantmap_engine.py           Ensemble de méthodes variées                                                                                                                   plantMapEngine(__init__, get_description, project_path, get_project, get_all_field_from_project, check_project_name, parsingKeyWords, edit_taxon_tab, load_xml, ) ObjectJSON(to_JSON)
plantMapXML.py               Création,  lecture des projet (XML)                                                                                                            plantMapXML(xml_writer, parse_xml, prettify)
project.py                   This class represents a project of the plugin                                                                                                  Project(__init__)
timer.py                     This class calculate the time and the percent for finish a process                                                                             Timer(__init__, newTurn, computeTimeProgress, computePercentProgress)
==========================   ============================================================================================================================================   ====================================================================================================================

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Les fichiers de configurations / métadonnées
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Ces fichiers permettent de configurer le plugin au besoin.

================  ===============================================================================================
Fichier           Description
================  ===============================================================================================
_project          XML décrivant le plugin
_pydevproject     XML ?
icon.png          Icone pour le bouton du plugin dans l'interface de QGIS
LICENSE           GNU GENERAL PUBLIC LICENSE Version 3,  29 June 2007
metadata.txt      description du plugin affiché dans la bbliothèque des plugin
resources.py      The translation of the .qrc file described above to Python.
resources.qrc     The .xml document created by Qt Designer. Contains relative paths to resources of the forms.
================  ===============================================================================================

---------------------------------
Développement et déploiement
---------------------------------
  * Récupérez les sources sur le dépot Github du projet : https://github.com/Max77T/plantmap-plugin
  * Compilez le plugin en utilisant pyrcc4
  * Pour être identifié par QGIS, le plugin doit être placé dans le dossier C:\Users\[nom_de_l_utilisateur]\.qgis2\python\plugins (sous windows) ou .qgis2/python/plugins/ (sous linux)
  * Réalisez les modifications souhaitées
  
   * Modifier le fichier d'implémentation : plantmap.py
   * Modifier l'interface utilisateur à partir de PlantMap.ui avec Qt Designer
   
  * Utilisez Makefile tpour compiler le projet avec ses interfaces. Cete étape nécessite GNU make (gmake)
  * Réalisez les tests (make test)
  * Testez le plugin en l'activant dans le gestionnaire des extension de QGIS
  
Pour plus d'information, veuillez consulter le PyQGIS Developer Cookbook : http://www.qgis.org/pyqgis-cookbook/index.html

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Modifier la description du plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Cette partie a pour but de modifier la description du plugin à l’installation

.. image:: ./img/modifier_description.png

Il faut modifier le fichier metadata.txt présent dans les sources du plugin.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Compiler les intefaces
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Pour modifier une interface (UI), il est recommandé d’utiliser QtCreator4 qui permet à l’aide de drag and drop de widget de modifier l’interface.
La modification d’une ui nécessite une recompilation à l’aide de la commande suivante::
	
	pyuic4 plantmap_dialog_base.ui -o plantmap_dialog_base.py

