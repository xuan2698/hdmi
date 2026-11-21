def stimulus(rng, cycles):
    rows = []
    seq = [
        {'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 0, 'y': 1}, {'x': 1, 'y': 1},
        {'x': 0, 'y': 2}, {'x': 1, 'y': 2}, {'x': 0, 'y': 3}, {'x': 1, 'y': 3},
        {'x': 0, 'y': 4}, {'x': 1, 'y': 4}, {'x': 0, 'y': 5}, {'x': 1, 'y': 5},
        {'x': 0, 'y': 6}, {'x': 1, 'y': 6}, {'x': 0, 'y': 7}, {'x': 1, 'y': 7},
    ]
    for r in seq:
        if len(rows) >= cycles:
            break
        rows.append({'x': r['x'], 'y': r['y']})
    while len(rows) < cycles:
        x = rng.getrandbits(1)
        y = rng.randrange(8)
        row = {'x': x, 'y': y}
        if rng.random() < 0.3:
            row['mid'] = {'x': rng.getrandbits(1)}
        rows.append(row)
    return rows[:cycles]
