import json

from qgis.PyQt.QtWidgets import QApplication
from qgis.core import (
    QgsJsonExporter,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingOutputNumber,
    QgsProcessingOutputString,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterCrs,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
)


class CopyVectorAsGeoJSONAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    SELECTED_ONLY = "SELECTED_ONLY"
    TARGET_CRS = "TARGET_CRS"
    PRECISION = "PRECISION"
    PRETTY_FORMAT = "PRETTY_FORMAT"
    INCLUDE_ATTRIBUTES = "INCLUDE_ATTRIBUTES"
    FEATURE_COUNT = "FEATURE_COUNT"
    MESSAGE = "MESSAGE"

    def name(self):
        return "copy_vector_as_geojson"

    def displayName(self):
        return "Copy Vector as GeoJSON"

    def group(self):
        return "Clipboard"

    def groupId(self):
        return "clipboard"

    def shortHelpString(self):
        return "Copies a vector layer to the system clipboard as a GeoJSON FeatureCollection."

    def createInstance(self):
        return CopyVectorAsGeoJSONAlgorithm()

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.INPUT, "Input vector layer", types=[QgsProcessing.TypeVectorAnyGeometry]
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            self.SELECTED_ONLY, "Copy selected features only", defaultValue=False
        ))
        self.addParameter(QgsProcessingParameterCrs(
            self.TARGET_CRS, "Output coordinate reference system", defaultValue="EPSG:4326"
        ))
        self.addParameter(QgsProcessingParameterNumber(
            self.PRECISION, "Coordinate decimal precision",
            type=QgsProcessingParameterNumber.Integer, defaultValue=6,
            minValue=0, maxValue=15
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            self.INCLUDE_ATTRIBUTES, "Include attribute fields", defaultValue=True
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            self.PRETTY_FORMAT, "Use readable formatted GeoJSON", defaultValue=True
        ))
        self.addOutput(QgsProcessingOutputNumber(
            self.FEATURE_COUNT, "Number of copied features"
        ))
        self.addOutput(QgsProcessingOutputString(self.MESSAGE, "Result message"))

    def processAlgorithm(self, parameters, context, feedback):
        layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if layer is None or not layer.isValid():
            raise QgsProcessingException("Please select a valid vector layer.")

        selected_only = self.parameterAsBoolean(parameters, self.SELECTED_ONLY, context)
        target_crs = self.parameterAsCrs(parameters, self.TARGET_CRS, context)
        precision = self.parameterAsInt(parameters, self.PRECISION, context)
        include_attributes = self.parameterAsBoolean(
            parameters, self.INCLUDE_ATTRIBUTES, context
        )
        pretty = self.parameterAsBoolean(parameters, self.PRETTY_FORMAT, context)

        if not target_crs.isValid():
            raise QgsProcessingException("The selected output CRS is invalid.")

        if selected_only:
            total = layer.selectedFeatureCount()
            if total == 0:
                raise QgsProcessingException(
                    "No features are selected. Select features first or disable selected-only."
                )
            features = layer.getSelectedFeatures()
        else:
            total = layer.featureCount()
            features = layer.getFeatures()

        if total == 0:
            raise QgsProcessingException("The input layer does not contain any features.")

        exporter = QgsJsonExporter(layer, precision)
        exporter.setIncludeGeometry(True)
        exporter.setIncludeAttributes(include_attributes)
        exporter.setSourceCrs(layer.crs())
        exporter.setDestinationCrs(target_crs)

        exported = []
        skipped = 0
        for index, feature in enumerate(features):
            if feedback.isCanceled():
                break
            try:
                exported.append(json.loads(exporter.exportFeature(feature)))
            except Exception as error:
                skipped += 1
                feedback.reportError(f"Feature {feature.id()} was skipped: {error}")
            feedback.setProgress(int(((index + 1) / total) * 100))

        if not exported:
            raise QgsProcessingException("No features could be converted to GeoJSON.")

        collection = {
            "type": "FeatureCollection",
            "name": layer.name(),
            "features": exported,
        }
        if target_crs.authid() != "EPSG:4326":
            collection["crs"] = {
                "type": "name", "properties": {"name": target_crs.authid()}
            }

        text = json.dumps(
            collection,
            ensure_ascii=False,
            indent=2 if pretty else None,
            separators=None if pretty else (",", ":"),
        )
        QApplication.clipboard().setText(text)

        message = f"{len(exported)} feature(s) copied as GeoJSON to the clipboard."
        if skipped:
            message += f" {skipped} feature(s) were skipped."
        feedback.pushInfo(message)
        return {self.FEATURE_COUNT: len(exported), self.MESSAGE: message}
