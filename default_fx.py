def compile_default_fx():
    name = 'name'
    attr = 'attr'
    kf_arc = 'kf_arc'
    axis = 'axis'
    rotation = 'rotation_euler'
    location = 'location'
    scale = 'scale'
    effects = 'effects'

    default_fx = [
        {
            name: 'WIGGLE',
            attr: rotation,
            kf_arc: [(0, 0), (0.5, 1), (0.5, -0.5), (0.25, 0)],
            axis: ['z']
        },
        {
            name: 'MOVE',
            attr: location,
            kf_arc: [(0, 0), (0.5, 1), (0.5, 0)],
            axis: ['x', 'y']
        },
        {
            name: 'PUSH_IN',
            attr: location,
            kf_arc: [(0, 1), (1, -0.05), (0.25, 0)],
            axis: ['x']
        },
        {
            name: 'PUSH_OUT',
            attr: location,
            kf_arc: [(0, 0), (0.25, -0.02), (1, 1)],
            axis: ['x']
        },
        {
            name: 'FALL_IN',
            attr: location,
            kf_arc: [(0, 1), (1, -0.05), (0.25, 0)],
            axis: ['y']
        },
        {
            name: 'FALL_OUT',
            attr: location,
            kf_arc: [(0, 0), (0.25, -0.02), (1, 1)],
            axis: ['y']
        },
        {
            name: 'POP_IN',
            attr: scale,
            kf_arc: [(0, 0), (1, 1.1), (0.25, 1)],
            axis: ['x', 'y', 'z']
        },
        {
            name: 'POP_OUT',
            attr: scale,
            kf_arc: [(0, 1.1), (0.25, 1), (1, 0)],
            axis: ['x', 'y', 'z']
        },
        {
            name: 'NONE',
            attr: '',
            kf_arc: [],
            axis: []
        },
        {
            name: 'WOBBLE',
            effects: ['WIGGLE', 'MOVE']
        }
    ]
    return default_fx
