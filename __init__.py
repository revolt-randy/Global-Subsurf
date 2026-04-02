bl_info = {
    "name": "Global Subsurf Settings",
    "author": "revolt_randy",
    "version": (1, 5, 0),
    "blender": (3, 6, 5),
    "location": "View3D > Tools > Global Subsurf",
    "description": "Changes subsurf modifier level settings",
    "warning": "",
    "doc_url": "https://github.com/revolt-randy/Global-Subsurf",
    "tracker_url": "",
    "category": "Mesh"}

# Import From Files
if "bpy" in locals():
    import importlib
    importlib.reload(mesh_global_subsurf)
else:
    from .import mesh_global_subsurf
    #from . import SUBSURF_SETTINGS_OT_Operator
    #$from . import SUBSURF_SETTINGS_PT_Panel
    
import bpy

def register():
    bpy.utils.register_class(mesh_global_subsurf.SUBSURF_SETTINGS_OT_Operator)
    bpy.utils.register_class(mesh_global_subsurf.SUBSURF_SETTINGS_PT_Panel)
    bpy.utils.register_class(mesh_global_subsurf.subsurf_settings)

def unregister():
    bpy.utils.unregister_class(mesh_global_subsurf.SUBSURF_SETTINGS_OT_Operator)
    bpy.utils.unregister_class(mesh_global_subsurf.SUBSURF_SETTINGS_PT_Panel)
    bpy.utils.unregister_class(mesh_global_subsurf.subsurf_settings)    