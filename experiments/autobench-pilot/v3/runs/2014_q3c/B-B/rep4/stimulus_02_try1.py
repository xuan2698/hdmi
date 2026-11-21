def stimulus(rng, cycles):
    rows = []
    seq = [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
        (0, 0), (1, 4), (0, 3), (1, 2), (0, 1), (1, 0)
    ]
    for x, y in seq:
        rows.append({'x': x, 'y': y})
    while len(rows) < cycles:
        x = rng.getrandbits(1)
        y = rng.randrange(5)
        r = {'x': x, 'y': y}
        if rng.random() < 0.3:
            r['mid'] = {'x': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
