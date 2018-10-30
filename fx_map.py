import bpy
from collections import deque

class Singleton:
    instance = None
    def __new__(singleton):
        return super().__new__(singleton) if not singleton.instance else singleton.instance

class TextEffectsMap(Singleton):
    map = {}
    def __init__(self, default_fx=True):
        # TODO set slide, pop, other surrounding-letter-touching overshoots based on letter spacing
        if default_fx:
            self.create_fx(name='WIGGLE', attr='rotation_euler', kf_arc=[(0, 0), (0.5, 1), (0.5, -0.5), (0.25, 0)], axis=['z'])
            self.create_fx(name='PUSH_IN', attr='location', kf_arc=[(0, 1), (1, -0.05), (0.25, 0)], axis=['x'])
            self.create_fx(name='PUSH_OUT', attr='location', kf_arc=[(0, 0), (0.25, -0.02), (1, 1)], axis=['x'])
            self.create_fx(name='FALL_IN', attr='location', kf_arc=[(0, 1), (1, -0.05), (0.25, 0)], axis=['y'])
            self.create_fx(name='FALL_OUT', attr='location', kf_arc=[(0, 0), (0.25, -0.02), (1, 1)], axis=['y'])
            self.create_fx(name='POP_IN', attr='scale', kf_arc=[(0, 0), (1, 1.1), (0.25, 1)], axis=['x', 'y', 'z'])
            self.create_fx(name='POP_OUT', attr='scale', kf_arc=[(0, 1.1), (0.25, 1), (1, 0)], axis=['x', 'y', 'z'])
            self.create_fx(name='NONE', attr='', kf_arc=[], axis=[])

    def set_kf_arc(self, name, kf_arc):
        if type(kf_arc) != list:
            print("Failed to assign kf_arc to text_fx {0} - expected list".format(name))
            return
        if name in self.map:
            self.map[name]['kf_arc'] = kf_arc
            return True
        return False

    # TODO edit kf_arc list values for given effect

    def get_map(self):
        return self.map

    def keys(self):
        return self.map.keys()

    def values(self):
        return self.map.values()

    def normalize_name(self, name):
        if type(name) != str: return
        return name.upper().replace(" ", "_")

    def exists(self, name):
        if not name in self.map:
            print("Unrecognized effect name {0} in text effects fx_map".format(name))
            return False
        return True

    def get_fx_entry(self, name='', normalize=True):
        if normalize:
            name = self.normalize_name(name)
        if self.exists(name):
            return self.map[name]

    def get_compound_fx(self, name=''):
        normalized_name = self.normalize_name(name)
        effects = []
        # no known effect
        if not self.exists(normalized_name):
            return effects
        # known compound effect
        if type(self.map[normalized_name]) is list:
            try:
                effects = [self.map[effect_name] for effect_name in self.map[normalize_name]]
                return effects
            except:
                print("Error building compound fx list for effect {0}".format(normalized_name))
        # known individual effect
        else:
            effects.append(self.get_fx_entry(normalized_name, normalize=False))
            return effects

    def check_fx_vals(self, name, attr, kf_arc, axis):
        if type(name) == str and type(attr) == str and type(kf_arc) == list and type(axis) == list:
            return True
        return False

    def get_attrs(self, name=''):
        effects = self.get_compound_fx(name)
        fx_attrs = []
        def simplify_transform_attr(attr_name):
            if 'location' in attr_name:
                return 'location'
            elif 'rotation' in attr_name:
                return 'rotation'
            elif 'scale' in attr_name:
                return 'scale'
            else:
                return ''
        if effects:
            fx_attrs = {simplify_transform_attr(effect['attr']) for effect in effects}
        return list(fx_attrs)

    def create_compound_fx(self, name='', effects=[]):
        known_fx = []
        if name and effects:
            for effect in effects:
                if type(effect) is str and self.exists(effect):
                    known_fx.append(effect)
            self.map[name] = effects

    def add_compound_fx(self, effect, name=''):
        if self.exists(name) and self.exists(effect) and type(self.map[name]) is list:
            self.map[name].append(effect)

    def remove_compound_fx(self, effect, name=''):
        if self.exists(name) and self.exists(effect) and type(self.map[name]) is list and effect in self.map[name]:
            self.map[name].remove(effect)

    def create_fx(self, name='', attr='', kf_arc=[], axis=[]):
        if not self.check_fx_vals(name, attr, kf_arc, axis):
            print("Unable to map text fx {0} to {1} effect arc {2}".format(name, attr, kf_arc))
            return
        self.map[name] = {
            'name': name,
            'attr': attr,
            'kf_arc': kf_arc,
            'axis': axis
        }

    def set_fx(self, name='', attr='', kf_arc=[(0, 0), (1, 1)], axis=['x', 'y', 'z']):
        if not self.check_fx_vals(name, attr, kf_arc, axis):
            return
        self.map[name] = self.create_fx(name=name, attr=attr, kf_arc=kf_arc, axis=axis)
        return self.map[name]

    def format_effects_names_to_bpy_enum(self):
        fx_items = deque([])
        fx_names_alphasort = sorted(self.keys(), reverse=True)
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
