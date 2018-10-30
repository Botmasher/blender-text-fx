import bpy
import os
from bpy.utils import register_class, unregister_class
from . import ui
from . import props

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
    props.remove_text_fx_props()
    try:
        bpy.utils.register_class(props.TextFxProperties)
    except:
        bpy.utils.unregister_class(props.TextFxProperties)
        bpy.utils.register_class(props.TextFxProperties)
    try:
        bpy.utils.register_class(ui.TextFxOperator)
    except:
        bpy.utils.unregister_class(ui.TextFxOperator)
        bpy.utils.register_class(ui.TextFxOperator)
    try:
        bpy.utils.register_class(ui.TextFxPanel)
    except:
        bpy.utils.unregister_class(ui.TextFxPanel)
        bpy.utils.register_class(ui.TextFxPanel)
    props.create_text_fx_props()

def unregister():
    props.remove_text_fx_props()
    bpy.utils.unregister_class(bpy.types.TextFxProperties)
    bpy.utils.unregister_class(bpy.types.OBJECT_OT_text_fx)
    bpy.utils.unregister_class(ui.TextFxPanel)

if __name__ == '__main__':
    register()
