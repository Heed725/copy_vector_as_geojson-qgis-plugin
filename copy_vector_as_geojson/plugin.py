import json

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QApplication
from qgis.core import (
    Qgis,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem,
    QgsJsonExporter,
    QgsMapLayerType,
    QgsProject,
    QgsRectangle,
    QgsVectorLayer,
)

from .provider import CopyVectorAsGeoJSONProvider


class CopyVectorAsGeoJSONPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.bbox_action = None
        self.provider = None

    def tr(self, text):
        return QCoreApplication.translate("CopyVectorAsGeoJSON", text)

    def initGui(self):
        self.action = QAction(
            QIcon.fromTheme("edit-copy"),
            self.tr("Copy as GeoJSON"),
            self.iface.mainWindow(),
        )
        self.action.setToolTip(
            self.tr("Copy selected features, or the whole layer, as EPSG:4326 GeoJSON")
        )
        self.action.triggered.connect(self.copy_active_layer)

        # Adds the action to the Layers panel right-click menu for vector layers.
        self.iface.addCustomActionForLayerType(
            self.action, "", QgsMapLayerType.VectorLayer, True
        )

        self.bbox_action = QAction(
            QIcon.fromTheme("mActionZoomToLayer"),
            self.tr("Copy BBOX"),
            self.iface.mainWindow(),
        )
        self.bbox_action.setToolTip(
            self.tr("Copy the selected features' or layer's EPSG:4326 bounding box")
        )
        self.bbox_action.triggered.connect(self.copy_active_layer_bbox)
        # Registered second so it appears directly below Copy as GeoJSON.
        self.iface.addCustomActionForLayerType(
            self.bbox_action, "", QgsMapLayerType.VectorLayer, True
        )

        self.provider = CopyVectorAsGeoJSONProvider()
        from qgis.core import QgsApplication
        QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        if self.action is not None:
            self.iface.removeCustomActionForLayerType(self.action)
            self.action.deleteLater()
            self.action = None

        if self.bbox_action is not None:
            self.iface.removeCustomActionForLayerType(self.bbox_action)
            self.bbox_action.deleteLater()
            self.bbox_action = None

        if self.provider is not None:
            from qgis.core import QgsApplication
            QgsApplication.processingRegistry().removeProvider(self.provider)
            self.provider = None

    def copy_active_layer(self):
        layer = self.iface.layerTreeView().currentLayer()
        if not isinstance(layer, QgsVectorLayer) or not layer.isValid():
            self._notify("Please choose a valid vector layer.", Qgis.Warning)
            return

        selected_count = layer.selectedFeatureCount()
        selected_only = selected_count > 0
        total = selected_count if selected_only else layer.featureCount()
        features = layer.getSelectedFeatures() if selected_only else layer.getFeatures()

        if total == 0:
            self._notify("The layer does not contain any features.", Qgis.Warning)
            return

        try:
            exporter = QgsJsonExporter(layer, 6)
            exporter.setIncludeGeometry(True)
            exporter.setIncludeAttributes(True)
            exporter.setSourceCrs(layer.crs())
            exporter.setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:4326"))

            exported = []
            skipped = 0
            for feature in features:
                try:
                    exported.append(json.loads(exporter.exportFeature(feature)))
                except Exception:
                    skipped += 1

            if not exported:
                self._notify("No features could be converted to GeoJSON.", Qgis.Critical)
                return

            collection = {
                "type": "FeatureCollection",
                "name": layer.name(),
                "features": exported,
            }
            text = json.dumps(collection, ensure_ascii=False, indent=2)
            QApplication.clipboard().setText(text)

            scope = "selected feature(s)" if selected_only else "feature(s)"
            message = f"Copied {len(exported)} {scope} as GeoJSON."
            if skipped:
                message += f" Skipped {skipped}."
            self._notify(message, Qgis.Success)
        except Exception as error:
            self._notify(f"Could not copy GeoJSON: {error}", Qgis.Critical, 8)

    def copy_active_layer_bbox(self):
        layer = self.iface.layerTreeView().currentLayer()
        if not isinstance(layer, QgsVectorLayer) or not layer.isValid():
            self._notify("Please choose a valid vector layer.", Qgis.Warning)
            return

        selected_count = layer.selectedFeatureCount()
        selected_only = selected_count > 0

        try:
            if selected_only:
                extent = QgsRectangle()
                has_geometry = False
                for feature in layer.getSelectedFeatures():
                    geometry = feature.geometry()
                    if geometry is None or geometry.isNull() or geometry.isEmpty():
                        continue
                    if not has_geometry:
                        extent = geometry.boundingBox()
                        has_geometry = True
                    else:
                        extent.combineExtentWith(geometry.boundingBox())

                if not has_geometry:
                    self._notify(
                        "The selected features do not contain geometry.", Qgis.Warning
                    )
                    return
            else:
                if layer.featureCount() == 0:
                    self._notify("The layer does not contain any features.", Qgis.Warning)
                    return
                extent = layer.extent()

            destination = QgsCoordinateReferenceSystem("EPSG:4326")
            transform = QgsCoordinateTransform(
                layer.crs(), destination, QgsProject.instance()
            )
            bbox = transform.transformBoundingBox(extent)
            values = [
                round(bbox.xMinimum(), 6),
                round(bbox.yMinimum(), 6),
                round(bbox.xMaximum(), 6),
                round(bbox.yMaximum(), 6),
            ]
            QApplication.clipboard().setText(json.dumps(values))

            scope = "selected features" if selected_only else "layer"
            self._notify(f"Copied {scope} BBOX as EPSG:4326: {values}", Qgis.Success)
        except Exception as error:
            self._notify(f"Could not copy BBOX: {error}", Qgis.Critical, 8)

    def _notify(self, message, level, duration=5):
        self.iface.messageBar().pushMessage(
            "Copy as GeoJSON", message, level=level, duration=duration
        )
