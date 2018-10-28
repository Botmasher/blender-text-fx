class TextEffectsMaker:
    def __init__(self, fx_map):
        self.set_fx_map(fx_map)

    def set_fx_map(self, fx_map):
        """Update the TextEffectsMap instance used for effects data"""
        if type(fx_map) is not TextEffectsMap:
            return False
        self.fx_map = fx_map
        return True

    def get_fx_map(self):
        """Update the TextEffectsMap instance used for effects data"""
        return self.fx_map

    def is_text(self, obj):
        return obj and hasattr(obj, 'type') and obj.type == 'FONT'

    def create_letter(self, text, letter="", font=None):
        """Make letter data, letter object and link letter to scene"""
        if type(letter) is not str or type(text) is not str:
            return
        # letter data
        name = "\"{0}\"-letter-{1}".format(text, letter)
        letter_data = bpy.data.curves.new(name=name, type='FONT')
        letter_data.body = letter if letter != " " else ""
        # assign selected font
        if font and font in bpy.data.fonts:
            letter_data.font = bpy.data.fonts[font]
        # letter object
        letter_obj = bpy.data.objects.new(letter_data.name, letter_data)
        bpy.context.scene.objects.link(letter_obj)
        return letter_obj

    ## take txt input and turn it into single-letter text objects
    def string_to_letters(self, txt="", spacing=0.0, font=''):
        """Take a string and create an array of letter objects"""
        origin = (0, 0, 0)
        offset_x = 0
        letter_objs = []

        # create font curve object for each letter
        for l in txt:

            # letter data
            letter_obj = self.create_letter(txt, letter=l, font=font)

            # set offset and base spacing on letter width
            letter_obj.location = [offset_x, *origin[1:]]
            bpy.context.scene.update()
            letter_offset = letter_obj.dimensions.x + spacing
            offset_x += letter_offset

            # delete blank spaces
            if l == " ":
                for obj in bpy.context.scene.objects:
                    obj.select = False
                letter_obj.select = True
                bpy.ops.object.delete()
            else:
                letter_objs.append(letter_obj)

        return letter_objs

    def set_kf(self, obj, attr=None, value=None, frames_before=0, frames_after=0):
        """Keyframe an object's attribute to the given value, moving playhead
        frames_before first and frames_after later"""
        if not hasattr(obj, attr) or not hasattr(obj, 'keyframe_insert') or value == None:
            print("Failed to set keyframe on {0} for attribute {1}".format(obj, attr))
            return
        bpy.context.scene.frame_current += frames_before
        setattr(obj, attr, value)
        kf = obj.keyframe_insert(data_path=attr)
        bpy.context.scene.frame_current += frames_after
        return kf

    # construct fx
    def keyframe_letter_fx (self, font_obj, effect={}):
        """Keyframe an effect on a letter based on an fx dict

        fx = {
            'name': '',         # like 'SLIDE'
            'attr': '',         # attribute to set on obj (location, rotation, scale)
            'kf_arc': [],       # (frame_mult, value_mult) pairs
            'transform': {},    # location, rotation, scale magnitudes multiplied by value_mult and added to base value at each kf set
            'axis': [],         # direcitonal axes along which to apply transforms
            'length': 0,        # each letter anim's frame count - multiplied by frame_mult at each kf set
            'offset': 0         # gap between letter anims to stagger each letter's effect
        }
        """
        # TODO update fx map above to reflect passed-in effect from effects list, plus sibling transforms, axis

        if not hasattr(font_obj, 'type') or not hasattr(font_obj, 'parent') or font_obj.type != 'FONT' or not effect or not 'attr' in effect:
            print("Failed to keyframe letter effect on {0} - expected a font curve parented to a letter fx empty".format(font_obj))
            return

        if not hasattr(font_obj, effect['attr']):
            print("Failed to set letter effect keyframe on {1} - unrecognized attribute or value".format(font_obj, effect['attr']))
            return

        value_base = None
        transform_magnitude = None
        axis = [dir.lower() for dir in effect['axis']]
        if 'location' in effect['attr']:
            value_base = font_obj.location[:]
            transform_magnitude = effect['transforms']['location']
        elif 'rotation' in effect['attr']:
            value_base = font_obj.rotation_euler[:]
            transform_magnitude = effect['transforms']['rotation']
        elif 'scale' in effect['attr']:
            value_base = font_obj.scale[:]
            transform_magnitude = effect['transforms']['scale']
        else:
            print("Did not recognize attr {0} on text object {1} for known text effects".format(attr, obj))
            return

        # keyframe along effect arc
        print("Keyframing along {0} effect arc for letter {1}".format(effect['name'], font_obj))

        for kf_mults in effect['kf_arc']:
            # multiply user settings by effect factors to get each kf
            frame_mult = kf_mults[0]
            value_mult = kf_mults[1]
            kf_value = value_mult * transform_magnitude
            kf_frames = int(round(effect['length'] * frame_mult))

            target_transform = {'x': value_base[0], 'y': value_base[1], 'z': value_base[2]}

            if 'location' in effect['attr']:
                # calc fixed loc for all location kfs
                # TODO recalculate since all axes passed in, but some add 0.0
                for dir in axis:
                    try:
                        # transform magnitude for this direction relative to parent
                        new_fixed_target = getattr(font_obj.parent.location, dir) + kf_value
                        # global world object origin for this direction
                        world_origin = getattr(font_obj.matrix_world.translation, dir)
                        #  step to new value for this direction
                        dir_value = self.lerp_step(origin=world_origin, target=new_fixed_target, factor=value_mult)
                        # store keyframe values for all axes
                        target_transform = {k: v if k != dir else dir_value for k, v in target_transform.items()}
                    except:
                        # location not recognized
                        print("Did not recognize {0} axis '{1}' for text fx - failed to animate letters".format(effect['attr'], dir))
                        return
            elif 'rotation' in effect['attr']:
                # TODO double check clockwise/counterclockwise (plus vs minus)
                for dir in axis:
                    try:
                        dir_value = target_transform[dir] - kf_value
                        target_transform = {k: v if k != dir else dir_value for k, v in target_transform.items()}
                    except:
                        print("Did not recognize {0} axis '{1}' for text fx - failed to animate letters".format(effect['attr'], dir))
                        return
            elif 'scale' in effect['attr']:
                for dir in axis:
                    try:
                        dir_value = target_transform[dir] * kf_value
                        target_transform = {k: v if k != dir else dir_value for k, v in target_transform.items()}
                    except:
                        print("Did not recognize {0} axis '{1}' for text fx - failed to animate letters".format(effect['attr'], dir))
                        return
            else:
                print("Did not recognize attr {0} on text object {1} for known text effects".format(attr, obj))

            target_value = [target_transform['x'], target_transform['y'], target_transform['z']]
            self.set_kf(font_obj, attr=effect['attr'], value=target_value, frames_before=kf_frames)

        return font_obj

    def lerp_step(self, origin=0, target=1, factor=0):
        """Step interpolate between origin and target values by a delta factor"""
        return (origin + ((target - origin) * factor))

    def center_letter_fx(self, letters_parent):
        """Move fx letter parent to simulate switching from left aligned to center aligned text"""
        # TODO allow other alignments; account for global vs parent movement
        extremes = []
        extremes[0] = letters_parent[0].location.x
        extremes[1] = letters_parent[-1].location.x + letters_parent[-1].dimensions.x
        distance = extremes[1] - extremes[0]
        letters_parent.location.x -= distance
        return letters_parent

    def parent_anim_letters(self, letters, fx, parent=None, start_frame=0, kf_handler=keyframe_letter_fx):
        """Attach letters to fx parent and keyframe each letter's effect based on fx data"""
        kfs = []

        for effect in fx['effects']:

            effect['length'] = fx['length']
            effect['transforms'] = fx['transforms']

            for letter in letters:

                # attach to parent but remove offset
                if not parent:
                    print("Expected text fx letter parent for '{0}' but parent is {1}".format(letter, parent))
                    return
                letter.parent = parent
                letter.matrix_parent_inverse = parent.matrix_world.inverted()

                effect['attr'] and effect['kf_arc'] and kfs.append(self.keyframe_letter_fx(letter, effect))

                #print("Anim frames: {0} -- Anim offset: {1} -- Current frame: {2}".format(fx['length'], fx['offset'], bpy.context.scene.frame_current))

                bpy.context.scene.frame_current += fx['offset']

        return kfs

    def set_parent_location(self, obj=None, target=None, default=(0,0,0), use_cursor=True):
        """Set the parent"""
        if not obj: return
        if use_cursor:
            obj.parent.location = bpy.context.scene.cursor_location
        elif target:
            obj.parent.location = target
        else:
            obj.parent.location = default

    def is_transform_map(self, d, transform_keys=['location', 'rotation', 'scale']):
        """Check if map contains location, rotation, scale keys with transform values"""
        value_types = (float, int)
        if len(d.keys()) != len(transform_keys):
            return False
        for transform in transform_keys:
            if transform not in d:
                return False
            if type(d[transform]) not in value_types:
                return False
        return True

    def anim_txt(self, txt="", time_offset=1, fx_name='', anim_order="forwards", fx_deltas={}, anim_length=5, anim_stagger=0, spacing=0.0, font=''):
        # TODO use clockwise to set rot +- for transformed x,y,z
        if not (txt and type(txt) is str and fx_deltas != None):
            return

        if bpy.context.scene.objects.active:
            target_location = bpy.context.scene.objects.active
        else:
            target_location = bpy.context.scene.cursor_location

        # build letter objects
        letters = self.string_to_letters(txt, spacing=spacing, font=font)

        # check format of axis and delta maps
        if not self.is_transform_map(fx_deltas):
            return

        # build fx dict
        fx = {}
        effects = fx_map.get_compound_fx(fx_name)
        if not effects:
            print("Failed to find fx_map data for text effect: {0}".format(fx_name))
            return
        fx['name'] = fx_name
        fx['effects'] = effects
        fx['length'] = anim_length
        fx['offset'] = anim_stagger
        fx['transforms'] = fx_deltas    # magnitude only; axis set in effects map

        #offsets = [i * time_offset for i in range(len(letters))]
        #randomize and random.shuffle(offsets)
        start_frame = bpy.context.scene.frame_current

        # TODO think through tricky cases where fx have:
        # - staggered starts but ending at the same frame
        # - logarithmic staggered starts or ends
        # - randomizing or complex animations
        # - ...

        # set up parent for holding letters
        letters_parent = bpy.data.objects.new("text_fx", None)
        bpy.context.scene.objects.link(letters_parent)
        letters_parent.empty_draw_type = 'ARROWS'
        letters_parent.empty_draw_size = 1.0

        # store properties in empty
        letters_parent.text_fx.frames = anim_length
        letters_parent.text_fx.time_offset = anim_stagger
        letters_parent.text_fx.spacing = spacing
        letters_parent.text_fx.name = fx_name
        letters_parent.text_fx.text = txt

        # letter orders: front-to-back, back-to-front, random
        letter_orders = {
            'forwards': lambda l: [*l],
            'backwards': lambda l: reversed(l),
            'random': lambda l: random.sample(l, len(l))
        }
        letters = letter_orders.get(anim_order, lambda l: l)(letters)
        # if anim_order == 'random':
        #     random.shuffle(letters)
        # elif anim_order == 'backwards':
        #     letters = reversed(letters)
        # else:
        #     letters = letters

        # keyframe effect for each letter
        self.parent_anim_letters(letters, fx, parent=letters_parent, start_frame=start_frame)

        # move letters to calculated target
        letters and self.set_parent_location(obj=letters[0], target=target_location)

        bpy.context.scene.frame_current = start_frame

        return letters

    # TODO letters are created in line with cursor at least along y but parent is not

    def set_font(self, letters_parent, font_name):
        """Update the font for each letter in a text effect object"""
        if not hasattr(letters_parent, 'children'): return
        if not font_name in bpy.data.fonts: return
        for letter in letters_parent.children:
            letter.data.font = font_name
        return font_name

    def find_text_fx_src(self):
        """Return the active text fx object or scene if there is none"""
        scene = bpy.context.scene
        obj = scene.objects.active
        if obj and hasattr(obj, "text_fx") and self.is_text(obj) and obj.text_fx.text:
            return obj
        return scene
