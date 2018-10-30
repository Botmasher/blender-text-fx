import bpy
from collections import deque
from . import fx_map
from . import fx_maker
from . import default_fx

# TODO create and hook up a class for managing tying together fx
#   - fx_map format props enum, calling props, interfacing with fx_map and executing fx_maker
#   - call this class from props.py, ui.py, maybe __init__
#   - instantiate globally in __init__?
class TextEffectsManager:
    def __init__(self, fx_map=None, fx_maker=None):
        if hasattr(fx_map, 'keys') and hasattr(fx_map, 'create_fx'):
            self.fx_map = fx_map
        if hasattr(fx_maker, 'anim_txt'):
            self.fx_maker = fx_maker
        return

    def add_effect(self, effect):
        if type(effect) is not dict:
            return
        created_effect = self.fx_map.create_fx(
            name=effect['name'],
            attr=effect['attr'],
            kf_arc=effect['kf_arc'],
            axis=effect['axis']
        )
        return created_effect

    def add_effects(self, effects):
    # TODO set slide, pop, other surrounding-letter-touching overshoots based on letter spacing
        if not effects or type(effects) is not list:
            return

        created_effects = []
        for effect in effects:
            created_effect = self.add_effect(effect)
            created_effect and created_effects.append(created_effect)

        return created_effects

    def format_effects_names_to_bpy_enum(self):
        fx_items = deque([])
        fx_names_alphasort = sorted(self.fx_map.keys(), reverse=True)
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

def start_manager():
    try:
        new_fx_mgr = fx_mgr
    except:
        fx_map = fx_map.TextEffectsMap()
        fx_maker = fx_maker.TextEffectsMaker()
        default_effects = default_fx.compile_default_fx()
        new_fx_mgr = TextEffectsManager(fx_map=fx_map, fx_maker=fx_maker)
        new_fx_mgr.add_effects(default_effects)
    return new_fx_mgr

fx_mgr = start_manager()
