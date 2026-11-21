def stimulus(rng, cycles):
    rows = []
    seq = [
        (1, 0), (0, 0), (0, 1), (1, 0), (1, 1),
        (0, 0), (1, 1), (1, 1), (1, 0), (0, 1),
        (0, 0), (0, 0), (1, 0), (0, 0), (1, 1),
        (0, 1)
    ]
    for a, b in seq:
        if len(rows) >= cycles:
            break
        rows.append({'a': a, 'b': b})
    while len(rows) < cycles:
        r = rng.randrange(4)
        a = (r >> 1) & 1
        b = r & 1
        row = {'a': a, 'b': b}
        if rng.random() < 0.3:
            row['mid'] = {'a': rng.getrandbits(1), 'b': rng.getrandbits(1)}
        rows.append(row)
    return rows[:cycles]
