# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from qgis.core import QgsProcessing, QgsProcessingAlgorithm, QgsProcessingMultiStepFeedback, QgsProcessingParameterVectorLayer, QgsProcessingParameterFileDestination, QgsProcessingParameterMultipleLayers, QgsProcessingParameterNumber, QgsProcessingParameterVectorDestination
from qgis.core import QgsGeometry, QgsVectorLayer, QgsFeature, QgsVectorFileWriter, QgsFields, QgsWkbTypes, QgsCoordinateReferenceSystem, QgsFields, QgsField, QgsDistanceArea
from qgis.PyQt.QtCore import QVariant

from io import StringIO
import matplotlib.pyplot as plt
from statistics import mean

from Comparator.yattag import Doc, indent

import processing

class Comparator(QgsProcessingAlgorithm): 

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('lignes', 'Profils à comparer', types=[QgsProcessing.TypeVectorLine]))
        self.addParameter(QgsProcessingParameterMultipleLayers('rasters', 'Rasters d\'élévations', layerType=QgsProcessing.TypeRaster))
        self.addParameter(QgsProcessingParameterNumber('echantillons_nb', 'Nombre d\'échantillons', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=1000, defaultValue=100))
        self.addParameter(QgsProcessingParameterFileDestination('OUTPUT', 'Comparaison', 'HTML files (*.html)'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # variables propres à Processing
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        
        # entrées
        lignes = self.parameterAsVectorLayer(parameters, 'lignes', context)
        rasters = parameters['rasters']
        
        # sorties
        output = self.parameterAsFileOutput(parameters, 'OUTPUT', context)
        doc, tag, text, line = Doc().ttl()

        # paramètres
        echantillons_nb = parameters['echantillons_nb']
        
        # traitement

        # si aucun raster n'est fourni en entrée, on quitte le traitement
        if len(rasters) == 0:
            feedback.pushInfo("⚠ Il est nécessaire de fournir au moins un raster en entrée.\n")
            return {}

        #
        # Discrétisation des valeurs des rasters sur les lignes
        #

        profils = []

        # on traite chaque ligne
        for ligne_f in lignes.getFeatures():

            ligne_g = ligne_f.geometry()
            freq = ligne_g.length()/(echantillons_nb-1)

            # création des points sur la ligne
            echantillons_g = [QgsGeometry().fromPointXY(ligne_g.asPolyline()[0])] # ajout d'un point en début de ligne
            for i in range(1, echantillons_nb-1):
                echantillons_g.append(ligne_g.interpolate(freq*i)) # ajout des points intermédiaires
            echantillons_g.append(QgsGeometry().fromPointXY(ligne_g.asPolyline()[-1])) # ajout d'un point en fin de ligne
            distance = QgsDistanceArea().measureLine(echantillons_g[0].asPoint(), echantillons_g[1].asPoint()) # distance entre les points
            feedback.pushInfo(str(echantillons_g))
            feedback.pushInfo("Distance entre les points : %s"%distance)

            # récupération de la valeur du raster sur chaque point
            rligne = []
            for raster in rasters:
                elevations = []
                for echantillon_g in echantillons_g:                
                    elevation = raster.dataProvider().sample(echantillon_g.asPoint(), 1)[0]
                    elevations.append(elevation)
                rligne.append({'nom':raster.name(), 'altitudes':elevations})

            profils.append({'nom':ligne_f.attributes()[0], 'distance':distance, 'rasters':rligne})
            
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        #
        # Création du rapport HTML
        #

        diffs = []
        svg_elv = []
        svg_diff = []

        for profil in profils:

            nom_ligne = profil['nom']
            distance = profil['distance']
            
            elv_plot = plt.figure()    
            for raster in profil['rasters']:
                plt.plot([round(distance*i) for i in range(echantillons_nb)], raster['altitudes'], label=raster['nom'])

            plt.xticks([round(distance*i) for i in range(echantillons_nb) if i in [0, round(echantillons_nb/4), round(echantillons_nb/2), round(3*echantillons_nb/4), echantillons_nb-1]])
            plt.legend()
            plt.xlabel('Distance sur la ligne (m)')
            plt.ylabel('Altitude (m)')
            buff = StringIO()
            elv_plot.savefig(buff, format='svg')
            buff.seek(0)
            svg_elv.append(buff.getvalue())

            diff = []
            diff_plot = plt.figure()
            for i in range(len(profil['rasters'][0]['altitudes'])):
                altis = [profil['rasters'][j]['altitudes'][i] for j in range(len(profil['rasters']))]
                diff.append(self.meanDev(altis))
            plt.plot([round(distance*i) for i in range(echantillons_nb)], diff, label='Écarts d\'altitudes moyens')
            plt.xticks([round(distance*i) for i in range(echantillons_nb) if i in [0, round(echantillons_nb/4), round(echantillons_nb/2), round(3*echantillons_nb/4), echantillons_nb-1]])
            plt.legend()
            plt.xlabel('Distance sur la ligne (m)')
            plt.ylabel('Écart moyen (m)')
            buff = StringIO()
            diff_plot.savefig(buff, format='svg')
            buff.seek(0)
            svg_diff.append(buff.getvalue())
            diffs.append(diff)

        # écriture du rapport HTML
        with tag('html'):
            with tag('head'):
                with tag('style'):
                    text('p, h1 { margin: 10px; } table, th, td { border-collapse: collapse; border: 1px solid black; padding: 5px; }')
            with tag('body'):
                i_ligne = 0
                for profil, elv_plot, diff_plot , diff in zip(profils, svg_elv, svg_diff, diffs): # traitement par pont
                    line('h1', profil['nom'])
                    doc.asis(elv_plot)
                    doc.asis(diff_plot)
                    with tag('p'):
                        doc.asis('<strong>Écart max</strong> :   %s m<br/>'%round(max(diff), 2))
                        doc.asis('<strong>Écart min</strong> :   %s m<br/>'%round(min(diff), 2))
                        doc.asis('<strong>Écart moyen</strong> : %s m<br/>'%round(mean(diff), 2))
        file = open(output, "w")
        file.write(indent(doc.getvalue()))
        file.close()
            
        feedback.setCurrentStep(2)
        
        results['OUTPUT']=output
        return results
                

    def name(self):
        return 'Comparer des rasters d\'altitude'

    def displayName(self):
        return 'Comparer des rasters d\'altitude'

    def createInstance(self):
        return Comparator()

    def meanDev(self, l):
        diffs = []
        for i in range(len(l)):
            for j in range(i, len(l)):
                if i != j:
                    diffs.append(abs(l[i]-l[j]))
        return mean(diffs)