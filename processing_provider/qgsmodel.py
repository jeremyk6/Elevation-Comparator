from qgis.core import QgsProcessingProvider, QgsProcessingModelAlgorithm
from qgis.PyQt.QtGui import QIcon


class Model(QgsProcessingModelAlgorithm):

    def icon(self):
        return self.img