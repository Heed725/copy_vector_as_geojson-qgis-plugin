# Copy Vector as GeoJSON — QGIS plugin

Adds **Copy as GeoJSON** and **Copy BBOX** to the right-click menu of every
vector layer in QGIS.

## Install

1. Open QGIS.
2. Go to **Plugins → Manage and Install Plugins**.
3. Choose **Install from ZIP**.
4. Select `copy_vector_as_geojson.zip` and click **Install Plugin**.
5. If necessary, enable **Copy Vector as GeoJSON** under **Installed**.

## Use

1. In the **Layers** panel, right-click a vector layer.
2. Click **Copy as GeoJSON** or **Copy BBOX**.
3. Paste with **Ctrl+V** into Notepad, VS Code, geojson.io, or another app.

If the layer has selected features, only those features are copied. If nothing
is selected, the full layer is copied. The context-menu command uses EPSG:4326,
six decimal places, readable formatting, and includes all attributes.

**Copy BBOX** copies a GeoJSON-style bounding-box array in this order:
`[minX, minY, maxX, maxY]`. It also uses selected features when present and the
full layer otherwise.

For configurable CRS, precision, formatting, and attributes, open the
**Processing Toolbox → GeoJSON Tools → Clipboard → Copy Vector as GeoJSON**.
