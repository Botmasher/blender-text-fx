import bpy
import os
from bpy.utils import register_class, unregister_class
from . import ui

bl_info = {
    "name": "Text FX",
    "description": "Text effects data and letter-by-letter transforms",
    "author": "Joshua R",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "View3D",
    "tracker_url": "https://github.com/Botmasher/blender-text-fx/issues",
    "support": "COMMUNITY",
    "category": "3D View"
}

def register():
    ui.remove_text_fx_props()
    bpy.utils.register_class(ui.TextFxProperties)
    bpy.utils.register_class(ui.TextFxOperator)
    bpy.utils.register_class(ui.TextFxPanel)
    ui.create_text_fx_props()

def unregister():
    ui.remove_text_fx_props()
    bpy.utils.unregister_class(bpy.types.TextFxProperties)
    bpy.utils.unregister_class(bpy.types.OBJECT_OT_text_fx)
    bpy.utils.unregister_class(ui.TextFxPanel)

if __name__ == '__main__':
    register()
