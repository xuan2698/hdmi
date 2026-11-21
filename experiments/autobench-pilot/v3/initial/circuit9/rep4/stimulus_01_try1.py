def stimulus(rng, cycles):
    rows = []
    rows.append({'a': 1})
    rows.append({'a': 1})
    rows.append({'a': 1})
    rows.append({'a': 1})
    rows.append({'a': 1})
    rows.append({'a': 1})
    rows.append({'a': 1})
    rows.append({'a': 1})
    rows.append({'a': 0})
    rows.append({'a': 0})
    rows.append({'a': 0})
    rows.append({'a': 0})
    rows.append({'a': 0})
    rows.append({'a': 0})
    rows.append({'a': 0})
    rows.append({'a': 0})
    while len(rows) < cycles:
        r = rng.randrange(4)
        if r == 0:
            rows.append({'a': 1})
        elif r == 1:
            rows.append({'a': 0})
        elif r == 2:
            rows.append({'a': rng.getrandbits(1)})
        else:
            rows.append({'a': rng.choice([0, 1]), 'mid': {'a': rng.choice([0, 1])}})
    return rows[:cycles]
