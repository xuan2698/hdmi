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
        rows.append(dict(r))
    while len(rows) < cycles:
        y = rng.randrange(8)
        x = rng.getrandbits(1)
        d = {'x': x, 'y': y}
        if rng.random() < 0.5:
            d['mid'] = {'x': 1 - x}
        rows.append(d)
    return rows[:cycles]
