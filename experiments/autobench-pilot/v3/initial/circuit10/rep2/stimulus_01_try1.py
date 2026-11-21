def stimulus(rng, cycles):
    rows = []
    seq = [
        (1, 0), (0, 0), (0, 1), (1, 0), (1, 1),
        (0, 0), (1, 1), (1, 1), (1, 0), (0, 1),
        (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
        (0, 0)
    ]
    for a, b in seq:
        rows.append({'a': a, 'b': b})
    while len(rows) < cycles:
        r = rng.randrange(4)
        a = (r >> 1) & 1
        b = r & 1
        row = {'a': a, 'b': b}
        if rng.randrange(3) == 0:
            row['mid'] = {'a': rng.getrandbits(1), 'b': rng.getrandbits(1)}
        rows.append(row)
    return rows[:cycles]
