=========================
Bugs connus
=========================
Lors de notre développement de ce projet nous avons rencontrés différents bug au sein de notre plugin que nous n’avons pas eu le temps de résoudre :

---------------
Nom de session
---------------
Lorsque l’utilisateur Windows possède un nom de session comportant des caractères spéciaux, le plugin rend une erreur à QGIS ::
  
	"warning:%s\ntraceback:%s" % (warnings.formatwarning(message, category, filename, lineno), stk),
	UnicodeDecodeError: 'ascii' codec can't decode byte ...

Ce problème est apparemment connu de la communauté Qgis  
(http://www.forumsig.org/showthread.php/40777-Probl%C3%A8me-d-acc%C3%A8s-Processing-Python?p=335480).

-------------------------------
Filtre des couches raster
-------------------------------
Le plugin ne filtre pas les couches raster. Si l’utilisateur sélectionne une couche raster au sein de l’onglet génération du plugin, le plugin affiche l’erreur  ::

	'QgsRasterLayer' object has no attribute 'pendingFields'

Il faudrait filtrer les rasters dans les propositions de couche.

----------------------
Encodage
----------------------
Il est possible que certaine partie de code traite mal les caractères spéciaux et que le plugin lève une exception. Lors de la sortie de Qgis 3.0 prenant en charge Python 3, les erreurs d’unicode devrait être résolues.
