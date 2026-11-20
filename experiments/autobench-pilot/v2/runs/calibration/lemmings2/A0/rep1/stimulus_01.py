def stimulus(rng, cycles):
    result = []
    state = 'walk_left'
    falling = False
    prev_ground = 1
    for i in range(cycles):
        areset = 0
        bump_left = 0
        bump_right = 0
        ground = 1
        if i == 0:
            areset = 1
        else:
            r = rng.randrange(100)
            if r < 5:
                areset = 1
            elif r < 20:
                bump_left = 1
            elif r < 35:
                bump_right = 1
            elif r < 45:
                bump_left = 1
                bump_right = 1
            elif r < 60:
                ground = 0
            elif r < 70:
                ground = 0
                bump_left = 1
            elif r < 80:
                ground = 0
                bump_right = 1
            elif r < 85:
                ground = 0
                bump_left = 1
                bump_right = 1
            else:
                ground = 1
        result.append({
            'areset': areset,
            'bump_left': bump_left,
            'bump_right': bump_right,
            'ground': ground,
        })
    return result
