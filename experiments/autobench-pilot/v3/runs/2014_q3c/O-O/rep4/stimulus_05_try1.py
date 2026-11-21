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
    for i in range(cycles):
        if i < len(seq):
            r = dict(seq[i])
        else:
            r = {'x': rng.getrandbits(1), 'y': rng.randrange(8)}
        if i % 3 == 1:
            r['mid'] = {'x': 1 - r['x']}
        elif i % 5 == 2:
            r['mid'] = {'y': rng.randrange(8)}
        rows.append(r)
    return rows
