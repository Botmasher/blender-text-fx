import bpy
from . import fx_manager
from . import props

# TODO layer effects vs replace effects
#   - are created fx mutable?
#   - replace each time vs stack effects?
#   - keep record of each object's effects and props for those fx?

# TODO handler to delete all letters on fx object deleted

class TextFxOperator(bpy.types.Operator):
    bl_label = "Text FX"
    bl_idname = "object.text_fx"
    bl_description = "Apply text effect"

    def execute(self, ctx):
        props_src = fx_manager.fx_mgr.fx_maker.find_text_fx_src()
        text_fx = props_src.text_fx

        # TODO add effect to obj vs create new obj
        #   - example: font changed

        # TODO list all modified attrs for compound fx
        modified_attrs = fx_manager.fx_mgr.fx_map.get_attrs(name=text_fx.effect)

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

        fx_manager.fx_mgr.fx_maker.anim_txt(text_fx.text, fx_manager.fx_mgr.fx_map, fx_name=text_fx.effect, font=text_fx.font, fx_deltas=transforms, anim_order=text_fx.letters_order, anim_stagger=text_fx.time_offset, anim_length=text_fx.frames, spacing=text_fx.spacing)

        return {'FINISHED'}

class TextFxPanel(bpy.types.Panel):
    bl_label = "Text FX Tools"
    bl_idname = "object.text_fx_panel"
    bl_category = "TextFX"
    bl_context = "objectmode"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, ctx):
        props_src = fx_manager.fx_mgr.fx_maker.find_text_fx_src()
        modified_attrs = fx_manager.fx_mgr.fx_map.get_attrs(name=props_src.text_fx.effect)

        if props_src:
            layout = self.layout
            text_fx = props_src.text_fx

            for prop_name in props.text_fx_prop_names:
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
