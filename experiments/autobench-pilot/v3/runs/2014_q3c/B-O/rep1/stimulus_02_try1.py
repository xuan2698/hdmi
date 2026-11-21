def stimulus(rng, cycles):
    rows = []
    seq = [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
        (0, 0), (1, 4), (0, 3), (1, 1), (0, 2), (1, 0)
    ]
    for x, y in seq:
        rows.append({'x': x, 'y': y})
    while len(rows) < cycles:
        r = rng.randrange(4)
        if r == 0:
            rows.append({'x': rng.getrandbits(1), 'y': rng.getrandbits(3)})
        elif r == 1:
            y = rng.choice([0, 1, 2, 3, 4])
            rows.append({'x': 0, 'y': y, 'mid': {'x': 1}})
        elif r == 2:
            y = rng.choice([0, 1, 2, 3, 4])
            rows.append({'x': 1, 'y': y, 'mid': {'x': 0}})
        else:
            rows.append({'x': rng.getrandbits(1), 'y': rng.choice([0, 1, 2, 3, 4])})
    return rows[:cycles]
