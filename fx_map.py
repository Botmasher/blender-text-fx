import bpy

# TODO: can a named effect be both non-compound transform and compound list?
#   - store effects key with list value alongside transform data
#   - would this allow for setting a custom "main" effect and a bunch of other ones? or any difference from just having single effects?
#   - or perhaps compound effects can store separate metaproperties

class Singleton:
    instance = None
    def __new__(singleton):
        return super().__new__(singleton) if not singleton.instance else singleton.instance

class TextEffectsMap(Singleton):
    def __init__(self):
        self.map = {}

    def update_kf_arc(self, name, kf_arc):
        """Update the keyframe arc in the transform data for the named effect"""
        if type(kf_arc) != list:
            print("Failed to assign kf_arc to text_fx {0} - expected list".format(name))
            return
        if name in self.map:
            self.map[name]['kf_arc'] = kf_arc
            return True
        return False

    def get_map(self):
        """Read all keys and values from the effects storage map"""
        return self.map

    def keys(self):
        """Read all keys from the effects storage map"""
        return self.map.keys()

    def values(self):
        """Read all values from the effects storage map"""
        return self.map.values()

    def normalize_name(self, name):
        """Format effect name variants as effects map names"""
        if type(name) != str: return
        return name.upper().replace(" ", "_")

    def exists(self, name):
        """"""
        if not name in self.map:
            print("Unrecognized effect name {0} in text effects fx_map".format(name))
            return False
        return True

    def get_fx_names(self, effect, check_compound=False):
        """List all effect names associated with the effect data"""
        # TODO select names from fx_map where effect == fx[name]
        matching_effects = []
        for effect_name, effect_value in self.map:
            if effect_value == effect:
                matching_effects.append(effect_name)
            elif check_compound and hasattr(self.map[effect_name]['effects']):
                for layered_effect in self.map[effect_name]['effects']:
                    and matching_effects.append(effect_name)
            else:
                pass
        return matching_effects

    def get_fx_entry(self, name='', normalize=True):
        """Read the stored data for this named effect"""
        if normalize:
            name = self.normalize_name(name)
        if self.exists(name):
            return self.map[name]

    # TODO update storiny compound effects list with kv effects: []
    def get_compound_fx(self, name=''):
        """List each effect's transform data associated with the named effect including all layered effects for compound effects"""
        normalized_name = self.normalize_name(name)
        effects = []
        # no known effect
        if not self.exists(normalized_name):
            return effects
        # known compound effect
        if hasattr(self.map[normalized_name], 'effects') and type(self.map[normalized_name]['effects']) is list:
            try:
                effects = [self.map[effect_name] for effect_name in self.map[normalized_name]['effects']]
                return effects
            except:
                print("Error building compound fx list for effect {0}".format(normalized_name))
        # known individual effect
        else:
            effects.append(self.get_fx_entry(normalized_name, normalize=False))
            return effects

    def is_compound_effect(self, name):
        """Check if the named effect stores data for a compound effect"""
        if self.exists(name) and hasattr(self.map[name], 'effects'):
            return True
        return False

    def check_fx_vals(self, name, attr, kf_arc, axis, relative):
        """Verify all of the data for a single non-compound effect"""
        if type(name) == str and type(attr) == str and type(kf_arc) == list and type(axis) == list and type(relative) == bool:
            return True
        print("Unable to set text fx \"{0}\" using attribute {1}, arc {2} and axis {3}".format(name, attr, kf_arc, axis))
        return False

    def get_attrs(self, name=''):
        """List all of the transform attributes modified by the named effect"""
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
        """Make a new effect that layers a list of named effects onto letters"""
        if not (name and effects):
            return
        known_fx = []
        for effect_name in effects:
            if type(effect_name) is str and self.exists(effect_name):
                known_fx.append(effect_name)
        self.map[name]['effects'] = known_fx
        return self.map[name]

    def reset_compound_fx(self, name='', effect_names=[]):
        """Replace the effect names list for the compound effect"""
        if not self.exists(name) and :
            return
        for effect_name in effect_names:
            if not self.exists(effect_name):
                return
        self.map[name]['effects'] = effect_names

    def add_compound_fx(self, effect_name, name=''):
        """Add effect name to the list of effects layered by the named compound effect"""
        if self.exists(name) and self.exists(effect_name) and self.is_compound_effect(name):
            self.map[name]['effects'].append(effect_name)

    def remove_compound_fx(self, effect_name, name=''):
        """Remove effect name from the list of effects layered by the named compound effect"""
        if self.exists(name) and self.exists(effect_name) and  self.is_compound_effect(name) and effect_name in self.map[name]['effects']:
            self.map[name]['effects'].remove(effect_name)

    def create_fx(self, name='', attr='', kf_arc=[], axis=[], relative=False):
        """Store a named non-compound effect with transform data"""
        if not self.check_fx_vals(name, attr, kf_arc, axis, relative):
            return
        self.map[name] = {
            'name': name,
            'attr': attr,
            'kf_arc': kf_arc,
            'axis': axis,
            'relative': relative
        }
        return self.map[name]

    def update_fx(self, name='', effect={}):
        """Update the stored transform data for a named non-compound effect"""
        if not self.exists(name):
            return
        try:
            self.create_fx(name, effect['attr'], effect['kf_arc'], effect['axis'], effect['relative'])
        except:
            print("fx_map.update_fx failed to update {0} with data {1}".format(name, effect))
            return
