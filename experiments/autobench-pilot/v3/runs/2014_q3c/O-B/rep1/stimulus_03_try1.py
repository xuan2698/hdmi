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
    for i in range(cycles):
        if i < len(seq):
            r = dict(seq[i])
        else:
            r = {'x': rng.getrandbits(1), 'y': rng.randrange(8)}
        if i % 3 == 1:
            r['mid'] = {'x': 1 - r['x']}
        rows.append(r)
    return rows
