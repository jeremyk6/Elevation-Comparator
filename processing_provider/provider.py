from qgis.core import QgsProcessingProvider, QgsProcessingModelAlgorithm
from qgis.PyQt.QtGui import QIcon

from Comparator import resources
from .algs.comparator import Comparator

import os
import glob

class Provider(QgsProcessingProvider):

    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(Comparator())
        for filename in glob.glob(os.path.join(os.path.dirname(__file__),"models", '*.model3')):
            alg = QgsProcessingModelAlgorithm()
            if not alg.fromFile(filename):
                print("Erreur : impossible de charger de modèle depuis {}".format(filename))
                return
            else:
                self.addAlgorithm(alg)
        

    def id(self, *args, **kwargs):
        return 'comparator'

    def name(self, *args, **kwargs):

        return 'Elevation Comparator'

    def icon(self):
        return QIcon(':/plugins/comparator/icon.png')