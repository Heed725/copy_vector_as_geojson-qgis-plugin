from qgis.core import QgsProcessingProvider

from .processing_algorithm import CopyVectorAsGeoJSONAlgorithm


class CopyVectorAsGeoJSONProvider(QgsProcessingProvider):
    def loadAlgorithms(self):
        self.addAlgorithm(CopyVectorAsGeoJSONAlgorithm())

    def id(self):
        return "geojson_tools"

    def name(self):
        return "GeoJSON Tools"

    def longName(self):
        return self.name()
