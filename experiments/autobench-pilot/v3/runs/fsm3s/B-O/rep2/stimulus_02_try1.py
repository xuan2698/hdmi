def stimulus(rng, cycles):
    rows = []
    seq = [
        {'reset': 1, 'in': 0},
        {'reset': 0, 'in': 0},
        {'reset': 0, 'in': 1},
        {'reset': 0, 'in': 1},
        {'reset': 0, 'in': 0},
        {'reset': 0, 'in': 1},
        {'reset': 0, 'in': 1},
        {'reset': 0, 'in': 1},
        {'reset': 0, 'in': 0},
        {'reset': 0, 'in': 0},
        {'reset': 0, 'in': 1},
        {'reset': 0, 'in': 0},
        {'reset': 0, 'in': 1},
        {'reset': 0, 'in': 1},
        {'reset': 0, 'in': 0},
        {'reset': 0, 'in': 1},
    ]
    for r in seq:
        if len(rows) >= cycles:
            break
        rows.append(dict(r))
    while len(rows) < cycles:
        r = {'reset': 0, 'in': rng.getrandbits(1)}
        if rng.random() < 0.3:
            r['mid'] = {'in': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
