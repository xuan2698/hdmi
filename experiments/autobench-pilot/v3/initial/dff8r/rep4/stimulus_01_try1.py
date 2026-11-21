def stimulus(rng, cycles):
    rows = []
    rows.append({'d': 0, 'reset': 1})
    rows.append({'d': 255, 'reset': 1})
    rows.append({'d': 0, 'reset': 0})
    rows.append({'d': 255, 'reset': 0})
    rows.append({'d': 0xAA, 'reset': 0})
    rows.append({'d': 0x55, 'reset': 0})
    rows.append({'d': 0x0F, 'reset': 0, 'mid': {'d': 0xF0}})
    rows.append({'d': 0xF0, 'reset': 0, 'mid': {'d': 0x0F}})
    rows.append({'d': 0x00, 'reset': 1, 'mid': {'reset': 0}})
    rows.append({'d': 0xFF, 'reset': 0, 'mid': {'reset': 1}})
    rows.append({'d': 0x81, 'reset': 0})
    rows.append({'d': 0x18, 'reset': 0})
    rows.append({'d': 0x3C, 'reset': 0, 'mid': {'d': 0xC3}})
    rows.append({'d': 0xC3, 'reset': 0, 'mid': {'d': 0x3C}})
    rows.append({'d': 0x7E, 'reset': 0})
    rows.append({'d': 0xE7, 'reset': 0})
    while len(rows) < cycles:
        r = rng.randrange(4)
        if r == 0:
            rows.append({'d': rng.getrandbits(8), 'reset': 1})
        elif r == 1:
            rows.append({'d': rng.getrandbits(8), 'reset': 0})
        elif r == 2:
            rows.append({'d': rng.getrandbits(8), 'reset': 0,
                         'mid': {'d': rng.getrandbits(8)}})
        else:
            rows.append({'d': rng.getrandbits(8), 'reset': rng.choice([0, 1]),
                         'mid': {'reset': rng.choice([0, 1])}})
    return rows[:cycles]
