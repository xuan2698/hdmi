def stimulus(rng, cycles):
    rows = []
    rows.append({'d': 0, 'reset': 1})
    rows.append({'d': 255, 'reset': 1})
    rows.append({'d': 0, 'reset': 0})
    rows.append({'d': 255, 'reset': 0})
    rows.append({'d': 170, 'reset': 0, 'mid': {'d': 85}})
    rows.append({'d': 85, 'reset': 0, 'mid': {'d': 170}})
    rows.append({'d': 1, 'reset': 0})
    rows.append({'d': 128, 'reset': 0})
    rows.append({'d': 0, 'reset': 1, 'mid': {'reset': 0}})
    rows.append({'d': 255, 'reset': 0, 'mid': {'reset': 1}})
    rows.append({'d': 0, 'reset': 0, 'mid': {'d': 255}})
    rows.append({'d': 255, 'reset': 0, 'mid': {'d': 0}})
    rows.append({'d': 42, 'reset': 0})
    rows.append({'d': 213, 'reset': 0})
    rows.append({'d': 0, 'reset': 1})
    rows.append({'d': 255, 'reset': 1})
    while len(rows) < cycles:
        r = rng.randrange(4)
        if r == 0:
            rows.append({'d': rng.getrandbits(8), 'reset': 1})
        elif r == 1:
            rows.append({'d': rng.getrandbits(8), 'reset': 0})
        elif r == 2:
            rows.append({'d': rng.getrandbits(8), 'reset': 0, 'mid': {'d': rng.getrandbits(8)}})
        else:
            rows.append({'d': rng.getrandbits(8), 'reset': rng.choice([0, 1]), 'mid': {'reset': rng.choice([0, 1])}})
    return rows[:cycles]
