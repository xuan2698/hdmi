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
    rows[1]['mid'] = {'x': 1 - rows[1]['x']}
    rows[3]['mid'] = {'x': 1 - rows[3]['x']}
    rows[5]['mid'] = {'x': 1 - rows[5]['x']}
    rows[7]['mid'] = {'x': 1 - rows[7]['x']}
    rows[9]['mid'] = {'x': 1 - rows[9]['x']}
    while len(rows) < cycles:
        y = rng.randrange(8)
        x = rng.getrandbits(1)
        d = {'x': x, 'y': y}
        if rng.random() < 0.5:
            d['mid'] = {'x': rng.getrandbits(1)}
        rows.append(d)
    return rows[:cycles]
