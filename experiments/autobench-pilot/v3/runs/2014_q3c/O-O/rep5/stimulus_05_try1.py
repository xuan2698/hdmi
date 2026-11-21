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
        rows.append(dict(r))
        if len(rows) >= cycles:
            return rows[:cycles]
    rows.append({'x': 0, 'y': 0b011, 'mid': {'x': 1}})
    rows.append({'x': 1, 'y': 0b100, 'mid': {'x': 0}})
    rows.append({'x': 0, 'y': 0b001, 'mid': {'x': 1}})
    rows.append({'x': 1, 'y': 0b010, 'mid': {'x': 0}})
    while len(rows) < cycles:
        rows.append({'x': rng.getrandbits(1), 'y': rng.randrange(8)})
    return rows[:cycles]
