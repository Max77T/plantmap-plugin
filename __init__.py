# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PlantMap
                                 A QGIS plugin
 This plugin provide a genertor of multitude maps
                             -------------------
        begin                : 2015-11-23
        copyright            : (C) 2015 by GreenMapper
        email                : maxencebunel77@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PlantMap class from file PlantMap.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .plantmap import PlantMap
    return PlantMap(iface)
