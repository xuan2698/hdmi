def stimulus(rng, cycles):
    rows = []
    seq = [
        {'a': 1, 'b': 0}, {'a': 0, 'b': 0}, {'a': 0, 'b': 1},
        {'a': 1, 'b': 0}, {'a': 1, 'b': 1}, {'a': 0, 'b': 0},
        {'a': 1, 'b': 1}, {'a': 1, 'b': 1}, {'a': 1, 'b': 0},
        {'a': 0, 'b': 1}, {'a': 0, 'b': 0}, {'a': 0, 'b': 0},
    ]
    for r in seq:
        rows.append(dict(r))
    while len(rows) < cycles:
        i = len(rows)
        if i % 7 == 0:
            r = {'a': rng.getrandbits(1), 'b': rng.getrandbits(1)}
            if rng.random() < 0.5:
                r['mid'] = {'a': rng.getrandbits(1), 'b': rng.getrandbits(1)}
            rows.append(r)
        elif i % 5 == 0:
            rows.append({'a': 1, 'b': 1})
        elif i % 3 == 0:
            rows.append({'a': 0, 'b': 0})
        else:
            rows.append({'a': rng.getrandbits(1), 'b': rng.getrandbits(1)})
    return rows[:cycles]
