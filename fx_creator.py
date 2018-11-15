import bpy
from . import fx_map
from . import default_fx
from bpy.props import *

# /!\ building - tasks are untested
# /!\ do not tie this into the main process

## NOTE: this "creator" is for creating and effect data stored in the "map"
##  - the "maker" is for applying effects to create text
##  - see TODO.md for namespace issues

class TextEffectsCreator:
    def __init__(self, mapper):
        self.fx_mapper = mapper
        return

    def is_axes_list(self, axes):
        """Check if a list contains valid axes"""
        compared_axes = ['x', 'y', 'z']
        valid_axes = [compared_axes.pop(axis) for axis in axes if axis in compared_axes]
        return (type(axes) is not list or len(valid_axes) != len(axes))

    def list_effects(self):
        """Get the names of all known effects - alias for fx_map.keys"""
        return self.mapper.keys()

    def create(self, fx_name, attr='', frame_arc=[], value_arc=[], axis=['x', 'y', 'z'], relative=False, compound=False, effects=[]):
        """Create a new effect with configured properties"""
        if not compound and (len(keyframe_arc) != len(value_arc) or not self.is_axes_list(axis)):
            return
        if compound:
            if type(effects) is not list:
                return
            effect = self.fx_mapper.create_compound_fx(fx_name, effects)
        else:
            kf_arc = []
            for i in range(len(frame_arc)):
                kf_arc.append([frame_arc[i], value_arc[i]])
            effect = self.fx_mapper.create_fx(fx_name, attr, kf_arc)
        return effect

effects_map = fx_map.TextEffectsMap()
fx_creator = TextEffectsCreator(fx_mapper)

# ui

# TODO instantiate props
prop_names = [
    'fx_name',
    'attr',
    'kf_arc_frames',
    'kf_arc_values',
    'axis',
    'relative',
    'compound',
    'effects'
]

class EffectsCreatorProperties(bpy.types.PropertyGroup):
    # TODO names, incrementing appended index, overwriting
    fx_name = StringProperty(name="Name", description="Name for the new effect", default="My Effect")
    attr = EnumProperty(
        name = "Transform",
        description = "Attribute to set during effect",
        items = [
            ("location", "Location", "Move letters"),
            ("rotation_euler", "Rotation", "Rotate letters"),
            ("scale", "Scale", "Scale letters")
        ],
        default='location'
    )
    # TODO variable list length
    kf_arc_frames = FloatVectorProperty(name="Arc frames", size=4, description="Percent of total frames to advance between each keyframe", default=(0.2, 0.3, 0.25, 0.25))
    kf_arc_values = FloatVectorProperty(name="Arc values", size=4, description="Percent of total value to set at each keyframe", default=(0.0, 0.5, 1.1, 1.0))
    # TODO pull in known effect names
    effects = StringVectorProperty(name="Effects", description="List of effects to compound", size=3, default=('WIGGLE', 'POP_IN', 'NONE'))
    relative = BoolProperty(name="Relative", description="Transform each letter using relative (each letter to/from its point) or fixed (all letters to/from same point) values", default=False)
    compound = BoolProperty(name="Compound", description="Toggle whether effect applies multiple other effects", default=False)
    axis = EnumProperty(
        name = "Axis",
        description = "Transform axis for effect",
        items = [
            ("z", "Z", "Transform along the z axis"),
            ("y", "Y", "Transform along the y axis"),
            ("x", "X", "Transform along the x axis"),
            ("xyz", "XYZ", "Transform along all axes"),
        ],
        default='xyz'
    )

class EffectsCreator(bpy.types.Operator):
    bl_label = "Text FX Creator"
    bl_idname = "object.text_fx_creator"
    bl_description = "Create and configure text effect"

    def execute(self, ctx):
        prop_src = scene.text_fx_creator
        # NOTE can wrap create call to pass in only prop_src
        fx_creator.create(prop_src.fx_name, attr=prop_src.attr, frame_arc=prop_src.kf_arc_frames, value_arc=prop_src.kf_arc_values, relative=prop_src.relative, compound=prop_src.compound, effects=prop_src.effects)
        return {'FINISHED'}

class EffectsCreatorPanel(bpy.types.Panel):
    bl_label = "Text FX Creator"
    bl_idname = "object.text_fx_creator_panel"
    bl_category = "TextFX Creator"
    bl_context = "objectmode"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, ctx):
        scene = ctx.scene
        layout = self.layout
        prop_src = scene.text_fx_creator
        is_compound = getattr(scene, 'compound')
        for prop_name in prop_names:
            if not is_compound and prop_name == 'effect':
                continue
            elif is_compound and prop_name in ['kf_arc_frames', 'kf_arc_values', 'axis', 'relative']:
                continue
            else:
                layout.row().prop(prop_src, prop_name)
        layout.operator('text_fx_creator', text="Store effect")
