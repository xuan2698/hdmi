def stimulus(rng, cycles):
    rows = []
    seq = [
        {'x': 0, 'y': 0},
        {'x': 1, 'y': 0},
        {'x': 0, 'y': 1},
        {'x': 1, 'y': 1},
        {'x': 0, 'y': 2},
        {'x': 1, 'y': 2},
        {'x': 0, 'y': 3},
        {'x': 1, 'y': 3},
        {'x': 0, 'y': 4},
        {'x': 1, 'y': 4},
        {'x': 0, 'y': 5},
        {'x': 1, 'y': 5},
        {'x': 0, 'y': 6},
        {'x': 1, 'y': 6},
        {'x': 0, 'y': 7},
        {'x': 1, 'y': 7},
    ]
    for r in seq:
        rows.append({'x': r['x'], 'y': r['y']})
    while len(rows) < cycles:
        r = rng.randrange(8)
        x = rng.getrandbits(1)
        row = {'x': x, 'y': r}
        if rng.random() < 0.5:
            row['mid'] = {'x': 1 - x}
        rows.append(row)
    return rows[:cycles]
