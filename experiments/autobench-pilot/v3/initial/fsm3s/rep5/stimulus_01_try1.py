def stimulus(rng, cycles):
    rows = []
    seq = [
        {'in': 0, 'reset': 1},
        {'in': 0, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 0, 'reset': 0},
        {'in': 0, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 0, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 0, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 0, 'reset': 0},
        {'in': 0, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 1, 'reset': 0},
    ]
    for r in seq:
        if len(rows) >= cycles:
            break
        rows.append(dict(r))
    while len(rows) < cycles:
        r = {'in': rng.getrandbits(1), 'reset': 0}
        if rng.randrange(8) == 0:
            r['reset'] = 1
        if rng.randrange(4) == 0:
            r['mid'] = {'in': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
