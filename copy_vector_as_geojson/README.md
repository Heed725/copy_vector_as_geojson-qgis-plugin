<p align="center">
  <img src="https://qgis.org/img/logosign.svg" alt="QGIS logo" width="110">
</p>

<h1 align="center">Copy Vector as GeoJSON</h1>

<p align="center">
  A convenient QGIS plugin for copying vector features and bounding boxes
  directly from the Layers panel.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/QGIS-3.22%2B-589632?style=for-the-badge&logo=qgis&logoColor=white" alt="QGIS 3.22+">
  <img src="https://img.shields.io/badge/Version-1.0.0-2E8B57?style=for-the-badge" alt="Version 1.0.0">
  <img src="https://img.shields.io/badge/Python-3-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/GeoJSON-Ready-5C4EE5?style=flat-square&logo=json&logoColor=white" alt="GeoJSON Ready">
  <img src="https://img.shields.io/badge/CRS-EPSG%3A4326-f39c12?style=flat-square" alt="EPSG:4326">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-555?style=flat-square" alt="Cross-platform">
  <img src="https://img.shields.io/badge/Status-Stable-brightgreen?style=flat-square" alt="Stable">
</p>

---

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
