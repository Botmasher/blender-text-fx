def compile_default_fx():
    name = 'name'
    attr = 'attr'
    kf_arc = 'kf_arc'
    axis = 'axis'
    rotation = 'rotation_euler'
    location = 'location'
    scale = 'scale'
    effects = 'effects'
    relative = 'relative'
    title = 'title'
    description = 'description'

    default_fx = [
        {
            name: 'WIGGLE',
            title: 'Wiggle',
            description: 'Add wiggle effect to text',
            attr: rotation,
            kf_arc: [(0, 0), (0.5, 1), (0.5, -0.5), (0.25, 0)],
            axis: ['z'],
            relative: True
        },
        {
            name: 'MOVE',
            title: 'Move',
            description: 'Add relative movement effect to text',
            attr: location,
            kf_arc: [(0, 0), (0.5, 1), (0.5, 0)],
            axis: ['x', 'y'],
            relative: True
        },
        {
            name: 'MOVE_HORIZ',
            title: 'Move horizontal',
            description: 'Add relative horizontal movement to text',
            attr: location,
            kf_arc: [(0, 0), (0.5, 1), (0.5, 0)],
            axis: ['y'],
            relative: True
        },
        {
            name: 'MOVE_VERT',
            title: 'Move vertical',
            description: 'Add relative vertical movement to text',
            attr: location,
            kf_arc: [(0, 0), (0.5, 1), (0.5, 0)],
            axis: ['x'],
            relative: True
        },
        {
            name: 'PUSH_IN',
            title: 'Push in',
            description: 'Slide text in from a fixed point',
            attr: location,
            kf_arc: [(0, 1), (1, -0.05), (0.25, 0)],
            axis: ['x'],
            relative: False
        },
        {
            name: 'PUSH_OUT',
            title: 'Push out',
            description: 'Slide text out to a fixed point',
            attr: location,
            kf_arc: [(0, 0), (0.25, -0.02), (1, 1)],
            axis: ['x'],
            relative: False
        },
        {
            name: 'FALL_IN',
            title: 'Fall in',
            description: 'Drop text in from a fixed point',
            attr: location,
            kf_arc: [(0, 1), (1, -0.05), (0.25, 0)],
            axis: ['y'],
            relative: False
        },
        {
            name: 'FALL_OUT',
            title: 'Fall out',
            description: 'Drop text out to a fixed point',
            attr: location,
            kf_arc: [(0, 0), (0.25, -0.02), (1, 1)],
            axis: ['y'],
            relative: False
        },
        {
            name: 'POP_IN',
            title: 'Pop in',
            description: 'Scale text up from nothing',
            attr: scale,
            kf_arc: [(0, 0), (1, 1.1), (0.25, 1)],
            axis: ['x', 'y', 'z'],
            relative: True
        },
        {
            name: 'POP_OUT',
            title: 'Pop out',
            description: 'Scale text down to nothing',
            attr: scale,
            kf_arc: [(0, 1.1), (0.25, 1), (1, 0)],
            axis: ['x', 'y', 'z'],
            relative: True
        },
        {
            name: 'NONE',
            title: 'None',
            description: 'Add no effect to the text',
            attr: '',
            kf_arc: [],
            axis: [],
            relative: False
        },
        {
            name: 'WOBBLE',
            title: 'Wobble',
            description: 'Wiggle and move text',
            effects: ['WIGGLE', 'MOVE']
        }
    ]
    return default_fx
