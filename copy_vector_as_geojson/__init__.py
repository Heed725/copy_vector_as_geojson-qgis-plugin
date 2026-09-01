def classFactory(iface):
    from .plugin import CopyVectorAsGeoJSONPlugin
    return CopyVectorAsGeoJSONPlugin(iface)
