# Copy Vector as GeoJSON v1.0.0

Initial stable release of **Copy Vector as GeoJSON**, a QGIS plugin for copying
vector data and bounding boxes directly from the Layers panel.

## Features

- Adds **Copy as GeoJSON** to the vector-layer right-click menu.
- Adds **Copy BBOX** directly below the GeoJSON command.
- Copies selected features when a selection exists.
- Copies the complete layer when no features are selected.
- Automatically transforms output to **EPSG:4326**.
- Includes feature attributes and geometry.
- Produces readable GeoJSON with six-decimal coordinate precision.
- Copies bounding boxes as `[minX, minY, maxX, maxY]`.
- Includes a configurable Processing Toolbox algorithm.
- Supports QGIS 3.22 and later on Windows, Linux, and macOS.

## Installation

1. Download `copy_vector_as_geojson.zip` from the GitHub release.
2. Open QGIS.
3. Select **Plugins → Manage and Install Plugins**.
4. Open **Install from ZIP**.
5. Select the downloaded ZIP and click **Install Plugin**.

## Usage

Right-click a vector layer in the QGIS Layers panel and choose:

- **Copy as GeoJSON** to copy features as a GeoJSON FeatureCollection.
- **Copy BBOX** to copy the layer or selection extent.

Paste the copied result into a text editor, VS Code, a browser console,
geojson.io, JavaScript, or another application using **Ctrl+V**.

## Requirements

- QGIS 3.22 or newer
- Python 3 supplied with QGIS

## Known behavior

When one or more features are selected, context-menu commands operate on the
selection. Clear the selection before copying if you want the complete layer.
