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
    for i in range(min(cycles, len(seq))):
        r = dict(seq[i])
        if i % 3 == 0:
            r['mid'] = {'x': 1 - r['x']}
        rows.append(r)
    while len(rows) < cycles:
        r = {'x': rng.getrandbits(1), 'y': rng.randrange(8)}
        if rng.random() < 0.5:
            r['mid'] = {'x': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
