def stimulus(rng, cycles):
    rows = []
    seq = [
        {'in': 0, 'reset': 1},
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
        {'in': 0, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 0, 'reset': 0},
        {'in': 1, 'reset': 0},
    ]
    rows.extend(seq)
    while len(rows) < cycles:
        r = rng.randrange(0, 100)
        if r < 10:
            rows.append({'in': rng.getrandbits(1), 'reset': 1})
        elif r < 20:
            rows.append({'in': rng.getrandbits(1), 'reset': 0, 'mid': {'in': rng.getrandbits(1)}})
        else:
            rows.append({'in': rng.getrandbits(1), 'reset': 0})
    return rows[:cycles]
