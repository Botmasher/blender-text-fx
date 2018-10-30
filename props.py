import bpy
from bpy.props import *
from . import fx_manager

# TODO set up props menu on empty (also shows up on letter select?)
#   - modify the existing fx
#   - update the text string
#       - accept text input directly
#       - accept named text_editor object

# UI checklist for prop names
# add, remove, reorder props to determine UI visibility
text_fx_prop_names = [
    'text',
    'font',
    'effect',
    'letters_order',
    'frames',
    'spacing',
    'time_offset',
    #'replace',
    'transform_location',
    #'axis_location',
    'transform_rotation',
    #'axis_rotation',
    'transform_scale',
    'clockwise'
]

class TextFxProperties(bpy.types.PropertyGroup):
    text = StringProperty(name="Text", description="Text that was split into animated letters", default="")
    font = StringProperty(name="Font", description="Loaded font used for letters in effect", default="Bfont")
    effect = EnumProperty(
        name = "Effect",
        description = "Overall effect to give when animating the letters",
        items = fx_manager.fx_mgr.format_effects_names_to_bpy_enum()
    )
    letters_order = EnumProperty(
        name = "Order",
        description = "Letter animation order",
        items = [
            ("random", "Random", "Animate text letters in random order"),
            ("backwards", "Backwards", "Animate text from last to first letter"),
            ("forwards", "Forwards", "Animate text from first to last letter")
        ]
    )
    frames = IntProperty(name="Frames", description="Frame duration of effect on each letter", default=10)
    spacing = FloatProperty(name="Spacing", description="Distance between letters", default=0.1)
    time_offset = IntProperty(name="Timing", description="Frames to wait between each letter's animation", default=1)
    replace = BoolProperty(name="Replace", description="Replace the current effect (otherwise added to letters)", default=False)
    transform_location = FloatProperty(name="Location change", description="Added value for letter location effect", default=1.0)
    transform_rotation = FloatProperty(name="Rotation change", description="Added value for letter rotation effect", default=1.0)
    transform_scale = FloatProperty(name="Scale change", description="Added value for letter scale effect", default=1.0)
    axis_location = EnumProperty(
        name = "Axis",
        description = "Transform axis for location effects",
        items = [
            ("z", "Z", "Move letters along the z axis"),
            ("y", "Y", "Move letters along the y axis"),
            ("x", "X", "Move letters along the x axis")
        ],
        default='x'
    )
    axis_rotation = EnumProperty(
        name = "Axis",
        description = "Transform axis for rotation effects",
        items = [
            ("z", "Z", "Rotate letters along the z axis"),
            ("y", "Y", "Rotate letters along the y axis"),
            ("x", "X", "Rotate letters along the x axis")
        ],
        default='z'
    )
    clockwise = BoolProperty(name="Clockwise", description="Rotate letters clockwise", default=True)

# props container
# - scene stores data before objects created
# - empty objects store created effect

def create_text_fx_props():
    bpy.types.Object.text_fx = bpy.props.PointerProperty(type=TextFxProperties)
    bpy.types.Scene.text_fx = bpy.props.PointerProperty(type=TextFxProperties)
    return

def remove_text_fx_props():
    try:
        del bpy.types.Object.text_fx
    except:
        print("Failed to delete text_fx props from bpy.types.Object. Ignore if first registration.")
    try:
        del bpy.types.Scene.text_fx
    except:
        print("Failed to delete text_fx props from bpy.types.Scene. Ignore if first registration.")
    return
