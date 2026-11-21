def stimulus(rng, cycles):
    rows = []
    seq = [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
        (0, 0), (1, 4), (0, 2), (1, 1), (0, 3), (1, 0)
    ]
    for x, y in seq:
        rows.append({'x': x, 'y': y})
    while len(rows) < cycles:
        r = rng.randrange(4)
        if r == 0:
            rows.append({'x': rng.getrandbits(1), 'y': rng.randrange(5)})
        elif r == 1:
            rows.append({'x': 0, 'y': rng.randrange(5), 'mid': {'x': 1}})
        elif r == 2:
            rows.append({'x': 1, 'y': rng.randrange(5), 'mid': {'x': 0}})
        else:
            rows.append({'x': rng.getrandbits(1), 'y': rng.randrange(5), 'mid': {'y': rng.randrange(5)}})
    return rows[:cycles]
