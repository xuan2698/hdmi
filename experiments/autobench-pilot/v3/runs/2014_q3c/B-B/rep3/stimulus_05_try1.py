def stimulus(rng, cycles):
    rows = [
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
        {'x': 0, 'y': 0b101},
        {'x': 1, 'y': 0b101},
        {'x': 0, 'y': 0b110},
        {'x': 1, 'y': 0b110},
        {'x': 0, 'y': 0b111},
        {'x': 1, 'y': 0b111},
    ]
    out = []
    for i in range(cycles):
        if i < len(rows):
            r = dict(rows[i])
        else:
            r = {'x': rng.getrandbits(1), 'y': rng.randrange(8)}
        if rng.random() < 0.3:
            r['mid'] = {'x': rng.getrandbits(1)}
        out.append(r)
    return out
