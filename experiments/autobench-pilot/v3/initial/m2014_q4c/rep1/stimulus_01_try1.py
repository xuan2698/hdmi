def stimulus(rng, cycles):
    rows = []
    rows.append({'d': 0, 'r': 1})
    rows.append({'d': 1, 'r': 1})
    rows.append({'d': 1, 'r': 0})
    rows.append({'d': 0, 'r': 0})
    rows.append({'d': 1, 'r': 0, 'mid': {'d': 0}})
    rows.append({'d': 0, 'r': 1, 'mid': {'r': 0}})
    rows.append({'d': 1, 'r': 1, 'mid': {'d': 0, 'r': 0}})
    rows.append({'d': 0, 'r': 0, 'mid': {'d': 1}})
    while len(rows) < cycles:
        i = len(rows)
        if i % 7 == 0:
            rows.append({'d': rng.getrandbits(1), 'r': 1})
        elif i % 7 == 1:
            rows.append({'d': rng.getrandbits(1), 'r': 0})
        elif i % 7 == 2:
            rows.append({'d': rng.choice([0, 1]), 'r': rng.choice([0, 1]),
                         'mid': {'d': rng.getrandbits(1)}})
        elif i % 7 == 3:
            rows.append({'d': rng.randrange(2), 'r': rng.randrange(2),
                         'mid': {'r': rng.getrandbits(1)}})
        elif i % 7 == 4:
            rows.append({'d': 1, 'r': 0, 'mid': {'d': 0, 'r': 1}})
        elif i % 7 == 5:
            rows.append({'d': 0, 'r': 1, 'mid': {'d': 1, 'r': 0}})
        else:
            rows.append({'d': rng.getrandbits(1), 'r': rng.getrandbits(1),
                         'mid': {'d': rng.getrandbits(1), 'r': rng.getrandbits(1)}})
    return rows[:cycles]
