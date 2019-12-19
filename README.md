# ![test](https://framagit.org/m2geonum/elevation-comparator/raw/master/icon.png) Elevation Comparator

Un plugin pour QGIS qui ajoute des modules traitements à Processing qui visent à permettre la comparaison entre plusieurs données d'élévation (MNS/MNT).

Les traitements développés :
* Analyser la précision : permet de comparer les valeurs d’un MNT avec les valeurs de points topographiques pour vérifier la qualité du MNT.
* Cartographier les changements : réalise une différence entre un MNT actuel et un MNT ancien par calcul raster et affiche le résultat de la comparaison à l’échelle de la bande active sélectionnée (polygone). Un style à appliquer au résultat [est fourni](https://framagit.org/m2geonum/elevation-comparator/raw/master/style/style.qml).
* Comparer des rasters d'altitude : réalise un rapport HTML graphique et statistique de changements entre plusieurs rasters d'altitudes.


Un [mode d'emploi](https://framagit.org/m2geonum/elevation-comparator/raw/release/Guide.pdf?inline=false) a été réalisé pour guider l'installation et l'utilisation du plugin.


Ce plugin a été développé et testé sous QGIS 3.10.


Il s'agit d'un travail réalisé lors d'un projet de Master 2 Géonum par Déodat Alindawa, Flavie Blard, Victor Bonnin, Marie Gradeler, Jérémy Kalsron.


![Logo Géonum](https://mastergeonum.files.wordpress.com/2019/09/cropped-rvb_originalsite.png?w=50&h=51)