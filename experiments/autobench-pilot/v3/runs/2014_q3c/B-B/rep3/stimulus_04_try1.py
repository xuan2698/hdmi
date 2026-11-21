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
        {'x': 0, 'y': 0b011, 'mid': {'x': 1}},
        {'x': 1, 'y': 0b100, 'mid': {'x': 0}},
        {'x': 0, 'y': 0b001, 'mid': {'y': 0b100}},
        {'x': 1, 'y': 0b010, 'mid': {'y': 0b001}},
        {'x': 0, 'y': 0b100, 'mid': {'x': 1, 'y': 0b011}},
        {'x': 1, 'y': 0b000, 'mid': {'x': 0, 'y': 0b010}},
    ]
    while len(rows) < cycles:
        r = rng.randrange(5)
        if r == 0:
            rows.append({'x': rng.getrandbits(1), 'y': rng.getrandbits(3)})
        elif r == 1:
            rows.append({'x': 0, 'y': rng.getrandbits(3)})
        elif r == 2:
            rows.append({'x': 1, 'y': rng.getrandbits(3)})
        elif r == 3:
            rows.append({'x': rng.getrandbits(1), 'y': rng.choice([0b000, 0b001, 0b010, 0b011, 0b100])})
        else:
            rows.append({'x': rng.getrandbits(1), 'y': rng.getrandbits(3), 'mid': {'x': rng.getrandbits(1)}})
    return rows[:cycles]
