import bpy
from collections import deque
from . import fx_map
from . import fx_maker
from . import default_fx

class TextEffectsManager:
    def __init__(self, map=None, maker=None):
        """Instantiate with an fx map (store effects) and maker (apply effects)"""
        if map and hasattr(map, 'keys') and hasattr(map, 'create_fx'):
            self.fx_map = map
        if maker and hasattr(maker, 'anim_txt'):
            self.fx_maker = maker
        return

    def add_effect(self, effect):
        """Add effect dict to effects map instance"""
        if type(effect) is not dict:
            return

        if 'effects' in effect and type(effect['effects']) is list:
            return self.fx_map.create_with_display_data(
                name=effect['name'],
                title=effect['title'],
                description=effect['description'],
                effects=effect['effects']
            )
        else:
            return self.fx_map.create_with_display_data(
                name=effect['name'],
                title=effect['title'],
                description=effect['description'],
                attr=effect['attr'],
                kf_arc=effect['kf_arc'],
                axis=effect['axis'],
                relative=effect['relative']
            )

    def add_effects(self, effects):
        """Add list of effects dicts to effects map instance"""
        # TODO set slide, pop, other surrounding-letter-touching overshoots based on letter spacing
        if not effects or type(effects) is not list:
            return

        created_effects = []
        for effect in effects:
            created_effect = self.add_effect(effect)
            created_effect and created_effects.append(created_effect)

        return created_effects

    def format_effects_names_to_bpy_enum(self):
        """Create formatted enum list for UI props"""
        fx_items = deque([])
        fx_names_alphasort = sorted(self.fx_map.keys(), reverse=True)
        for effect_name in fx_names_alphasort:
            effect_entry = self.fx_map.entry(effect_name)
            fx_item = (effect_name, effect_entry['title'], effect_entry['description'])
            if effect_name.lower() == 'none':
                fx_items.appendleft(fx_item)
                continue
            fx_items.append(fx_item)
        fx_items.reverse()
        return list(fx_items)

def start_manager():
    """Create or retrieve the fx manager with default effects"""
    try:
        new_fx_mgr = fx_mgr
    except:
        effect_describer = fx_map.TextEffectsMap()
        effect_creator = fx_maker.TextEffectsMaker()
        default_effects = default_fx.compile_default_fx()
        new_fx_mgr = TextEffectsManager(map=effect_describer, maker=effect_creator)
        new_fx_mgr.add_effects(default_effects)
    return new_fx_mgr

# NOTE dependency issues:
#   - props uses fx_mgr to format enums
#   - TextEffectsManager stores instance of map and one to maker
fx_mgr = start_manager()
