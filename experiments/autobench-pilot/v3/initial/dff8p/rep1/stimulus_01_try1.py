def stimulus(rng, cycles):
    rows = []
    rows.append({'d': 0x34, 'reset': 1})
    rows.append({'d': 0x00, 'reset': 1})
    rows.append({'d': 0xFF, 'reset': 1})
    rows.append({'d': 0x34, 'reset': 0})
    rows.append({'d': 0x00, 'reset': 0})
    rows.append({'d': 0xFF, 'reset': 0})
    rows.append({'d': 0x55, 'reset': 0, 'mid': {'d': 0xAA}})
    rows.append({'d': 0xAA, 'reset': 0, 'mid': {'d': 0x55}})
    rows.append({'d': 0x0F, 'reset': 1, 'mid': {'reset': 0}})
    rows.append({'d': 0xF0, 'reset': 0, 'mid': {'reset': 1}})
    rows.append({'d': 0x34, 'reset': 0, 'mid': {'d': 0x00}})
    rows.append({'d': 0x00, 'reset': 0, 'mid': {'d': 0xFF}})
    rows.append({'d': 0xFF, 'reset': 0, 'mid': {'d': 0x34}})
    rows.append({'d': 0x12, 'reset': 0, 'mid': {'d': 0xED}})
    rows.append({'d': 0xED, 'reset': 0, 'mid': {'d': 0x12}})
    rows.append({'d': 0x34, 'reset': 1, 'mid': {'d': 0x00, 'reset': 0}})
    while len(rows) < cycles:
        r = rng.randrange(4)
        if r == 0:
            rows.append({'d': rng.getrandbits(8), 'reset': 0})
        elif r == 1:
            rows.append({'d': rng.getrandbits(8), 'reset': 1})
        elif r == 2:
            rows.append({'d': rng.getrandbits(8), 'reset': rng.choice([0, 1]),
                         'mid': {'d': rng.getrandbits(8)}})
        else:
            rows.append({'d': rng.getrandbits(8), 'reset': rng.choice([0, 1]),
                         'mid': {'reset': rng.choice([0, 1])}})
    return rows[:cycles]
