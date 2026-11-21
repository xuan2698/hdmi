def stimulus(rng, cycles):
    rows = [
        {'x': 0, 'y': 0b000},
        {'x': 1, 'y': 0b000},
        {'x': 0, 'y': 0b001},
        {'x': 1, 'y': 0b001},
        {'x': 0, 'y': 0b010},
        {'x': 1, 'y': 0b010},
        {'x': 0, 'y': 0b011},
        {'x': 1, 'y': 0b011},
        {'x': 0, 'y': 0b100},
        {'x': 1, 'y': 0b100},
        {'x': 0, 'y': 0b000, 'mid': {'x': 1}},
        {'x': 1, 'y': 0b001, 'mid': {'x': 0}},
        {'x': 0, 'y': 0b011, 'mid': {'y': 0b100}},
        {'x': 1, 'y': 0b100, 'mid': {'y': 0b010}},
        {'x': 0, 'y': 0b010, 'mid': {'x': 1, 'y': 0b001}},
        {'x': 1, 'y': 0b011, 'mid': {'x': 0, 'y': 0b100}},
    ]
    out = []
    for i in range(cycles):
        if i < len(rows):
            r = dict(rows[i])
        else:
            r = {'x': rng.getrandbits(1), 'y': rng.randrange(8)}
            if rng.random() < 0.3:
                r['mid'] = {'x': rng.getrandbits(1)}
                if rng.random() < 0.5:
                    r['mid']['y'] = rng.randrange(8)
        out.append(r)
    return out
