import bpy
import random
from bpy.props import *
from collections import deque

## Text FX
## Blender Python script by Joshua R (Botmasher)
##
## Create letter-by-letter text effects
##
## NOTE: clarify semantics of "effects" / "fx" (used interchangeably)
##  - "effects" ambiguity: fx data vs fx'd letters vs fx letters parents
##
## Intended use:
##  - place a new text effect in the scene
##      - each effect has separate letter objects attached to an empty parent
##      - empty parent stores the fx props data
##  - modify (or simulate modification of) an existing text effect
##      - select text fx letters parent to retrieve data and change through UI
##
## Structure:
##  - tool ui:  text_fx props, panel, operator (including registration and prop assignment)
##  - fx data:  stored and accessed with TextEffectsMap
##  - fx logic: apply effects to create fx letters & parent
##

# TODO define axes on effects map instead of props
#   - changing axis may change fx, e.g. slide X/Y vs perspective Z
#   - allow action control in fx map data (rotate: wiggle Z vs turn Y)
