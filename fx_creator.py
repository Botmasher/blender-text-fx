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

fx_mapper = fx_map.TextEffectsMap()
fx_creator = TextEffectsCreator(fx_mapper)

# TODO ui

# panel

# operator
