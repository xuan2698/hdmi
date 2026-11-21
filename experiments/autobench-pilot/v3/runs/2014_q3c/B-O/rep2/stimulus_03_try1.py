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
        rows.append({'x': r['x'], 'y': r['y']})
    while len(rows) < cycles:
        y = rng.randrange(8)
        x = rng.getrandbits(1)
        d = {'x': x, 'y': y}
        if rng.random() < 0.3:
            d['mid'] = {'x': rng.getrandbits(1)}
        rows.append(d)
    return rows[:cycles]
