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
    while len(rows) < cycles:
        r = rng.randrange(5)
        if r == 0:
            rows.append({'x': rng.getrandbits(1), 'y': rng.getrandbits(3)})
        elif r == 1:
            rows.append({'x': 0, 'y': rng.getrandbits(3)})
        elif r == 2:
            rows.append({'x': 1, 'y': rng.getrandbits(3)})
        elif r == 3:
            y = rng.choice([0b000, 0b001, 0b010, 0b011, 0b100])
            rows.append({'x': rng.getrandbits(1), 'y': y})
        else:
            y = rng.choice([0b000, 0b001, 0b010, 0b011, 0b100])
            rows.append({'x': rng.getrandbits(1), 'y': y, 'mid': {'x': rng.getrandbits(1)}})
    return rows[:cycles]
