================
Introduction
================
PlantMap est une solution pour produire et partager un grand nombre de cartes en itérant sur une couche de données tout en conservant l'emprise géographique.

L'outil est composé d’un plugin QGIS permettant la génération de cartes et d’une application web vitrine exposant ces différentes créations.
La principale caractéristique du plugin est la génération de carte par combinaison d'un fond de plan statique et d'une source de données dynamique. En effet, l'utilisateur configure le modèle de carte qu'il souhaite réaliser grâce au composer d'impression de QGIS et le plugin permet alors de produire une carte accompagnée de ses métadonnées pour chacune des entités défini dans une couche spécifique. Le cas d'utilisation initial de ce plugin est la génération de carte de répartition d'espèce pour la flore.

La seconde partie de la solution (qui n'est pas documenté ici) consiste a exposer l'ensemble de ces cartes sur une plateforme Web. Les principales fonctions de cette plateforme sont : rechercher, importer, supprimer et télécharger des cartes. Les métadonnées générées par le plugin sont utilisées pour réaliser des recherches aux sein de la plateforme.