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
    ]
    for r in seq:
        rows.append(dict(r))
    while len(rows) < cycles:
        r = {'x': rng.getrandbits(1), 'y': rng.randrange(8)}
        if rng.random() < 0.5:
            r['mid'] = {'x': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
