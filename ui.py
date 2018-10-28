from . import fx_map
from . import fx_maker

# text fx instances
fx_map = fx_map.TextEffectsMap()        # data
fx = fx_maker.TextEffectsMaker(fx_map)  # logic

# TODO set up props menu on empty (also shows up on letter select?)
#   - modify the existing fx
#   - update the text string
#       - accept text input directly
#       - accept named text_editor object

def format_fx_enum():
    fx_items = deque([])
    fx_names_alphasort = sorted(fx_map.keys(), reverse=True)
    for k in fx_names_alphasort:
        item_name = "{0}{1}".format(k[0].upper(), k[1:].lower().replace("_", " "))
        if k.lower() == 'none':
            item_description = "Add no effect to text"
            fx_items.appendleft((k, item_name, item_description))
            continue
        item_description = "Add {0} effect to text".format(k.lower())
        fx_items.append((k, item_name, item_description))
    fx_items.reverse()
    return list(fx_items)

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
        items = format_fx_enum()
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

# TODO layer effects vs replace effects
#   - are created fx mutable?
#   - replace each time vs stack effects?
#   - keep record of each object's effects and props for those fx?

# TODO handler to delete all letters on fx object deleted

class TextFxOperator(bpy.types.Operator):
    bl_label = "Text FX"
    bl_idname = "object.text_fx"
    bl_description = "Create and configure text effect"

    def execute(self, ctx):
        props_src = fx.find_text_fx_src()
        text_fx = props_src.text_fx

        # TODO add effect to obj vs create new obj
        #   - example: font changed

        # TODO list all modified attrs for compound fx
        modified_attrs = fx_map.get_attrs(name=text_fx.effect)

        # compile map of all transform magnitude deltas
        # NOTE x,y,z now defined in effects map - originally set here
        transforms = {
            'location': text_fx.transform_location,
            'rotation': text_fx.transform_rotation,
            'scale': text_fx.transform_scale
        }
        if not text_fx.clockwise:
            transforms['rotation'] = -transforms['rotation']

        #for attr in effects_attrs:
        #   if not hasattr(obj, attr):
        #       print("No location/rotation/scale attr recognized for effect - cancelling text effect")
        #       return {'FINISHED'}

        fx.anim_txt(text_fx.text, fx_name=text_fx.effect, font=text_fx.font, fx_deltas=transforms, anim_order=text_fx.letters_order, anim_stagger=text_fx.time_offset, anim_length=text_fx.frames, spacing=text_fx.spacing)

        return {'FINISHED'}

class TextFxPanel(bpy.types.Panel):
    bl_label = "Text FX Tools"
    bl_idname = "object.text_fx_panel"
    bl_category = "TextFX"
    bl_context = "objectmode"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, ctx):
        props_src = fx.find_text_fx_src()
        modified_attrs = fx_map.get_attrs(name=props_src.text_fx.effect)

        if props_src:
            layout = self.layout
            text_fx = props_src.text_fx

            for prop_name in text_fx_prop_names:
                # fall back to scene data if letters prop is undefined
                if hasattr(text_fx, prop_name) and getattr(text_fx, prop_name) is not None:
                    fx_data = text_fx
                else:
                    fx_data = bpy.context.scene.text_fx

                if prop_name == 'font':
                    layout.prop_search(fx_data, prop_name, bpy.data, 'fonts')
                    # TODO load a new font not just select loaded font
                    #row = layout.split(percentage=0.25)
                    #row.template_ID(ctx.curve, prop_name, open="font.open", unlink="font.unlink")
                elif prop_name in ['transform_location', 'axis_location']:
                    'location' in modified_attrs and self.layout.row().prop(fx_data, prop_name)
                elif prop_name in ['transform_rotation', 'axis_rotation', 'clockwise']:
                    'rotation' in modified_attrs and self.layout.row().prop(fx_data, prop_name)
                elif prop_name == 'transform_scale':
                    'scale' in modified_attrs and self.layout.row().prop(fx_data, prop_name)
                else:
                    layout.row().prop(fx_data, prop_name)

            layout.row().operator("object.text_fx", text="Create Text Effect")

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
        print("Failed to delete text_fx props from bpy.types.Object")
    try:
        del bpy.types.Scene.text_fx
    except:
        print("Failed to delete text_fx props from bpy.types.Scene")
    return
