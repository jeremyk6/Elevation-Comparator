from qgis.core import QgsProcessingProvider, QgsProcessingModelAlgorithm
from qgis.PyQt.QtGui import QIcon

from Comparator import resources
from .algs.comparator import Comparator

import os
import glob

class Model(QgsProcessingModelAlgorithm):
    def __init__(self, path, icon):
        super(Model, self).__init__()
        self.img = icon
        self.fromFile(path)

    def icon(self):
        return self.img

class Provider(QgsProcessingProvider):

    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(Comparator())
        self.addAlgorithm(Model(os.path.join(os.path.dirname(__file__),"models", 'analyse_precision.model3'), QIcon(':/plugins/comparator/resources/precision.png')))
        self.addAlgorithm(Model(os.path.join(os.path.dirname(__file__),"models", 'rendu_carto.model3'), QIcon(':/plugins/comparator/resources/carto.png')))

    def id(self, *args, **kwargs):
        return 'comparator'

    def name(self, *args, **kwargs):

        return 'Elevation Comparator'

    def icon(self):
        return QIcon(':/plugins/comparator/icon.png')