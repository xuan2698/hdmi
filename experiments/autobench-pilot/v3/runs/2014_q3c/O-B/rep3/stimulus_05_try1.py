def stimulus(rng, cycles):
    rows = []
    seq = [
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
        {'x': 0, 'y': 0b011, 'mid': {'x': 1}},
        {'x': 1, 'y': 0b011, 'mid': {'x': 0}},
        {'x': 0, 'y': 0b100, 'mid': {'x': 1}},
        {'x': 1, 'y': 0b100, 'mid': {'x': 0}},
        {'x': 0, 'y': 0b001, 'mid': {'x': 1}},
        {'x': 1, 'y': 0b001, 'mid': {'x': 0}},
    ]
    for r in seq:
        if len(rows) >= cycles:
            break
        rows.append(dict(r))
    while len(rows) < cycles:
        y = rng.getrandbits(3)
        x = rng.getrandbits(1)
        r = {'x': x, 'y': y}
        if rng.random() < 0.5:
            r['mid'] = {'x': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
