bl_info = {
    "name": "Unity Bulk Asset Exporter",
    "description": "Export meshes, textures, materials and prefabs for Unity HDRP",
    "author": "Antigravity",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Unity Export",
    "category": "Import-Export",
}

import importlib
from . import main

importlib.reload(main)

def register():
    main.register()

def unregister():
    main.unregister()

if __name__ == "__main__":
    register()
