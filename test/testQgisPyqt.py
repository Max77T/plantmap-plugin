import os
import logging
import json
import sys
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox
from PyQt4.QtXml import QDomDocument
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from qgis.core import *
from qgis.utils import*
from threading import Thread, RLock
import time