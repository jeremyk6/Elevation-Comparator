from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from comparator import resources
from .comparator import Comparator

class Provider(QgsProcessingProvider):

    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(Comparator())

    def id(self, *args, **kwargs):
        return 'comparator'

    def name(self, *args, **kwargs):

        return 'Comparator'

    def icon(self):
        return QIcon(':/plugins/comparator/icon.png')