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
    rows.append({'d': 0x0F, 'reset': 0, 'mid': {'reset': 1}})
    rows.append({'d': 0xF0, 'reset': 1, 'mid': {'reset': 0}})
    rows.append({'d': 0x34, 'reset': 0, 'mid': {'d': 0x00}})
    rows.append({'d': 0x00, 'reset': 0, 'mid': {'d': 0x34}})
    while len(rows) < cycles:
        r = rng.randrange(4)
        d = rng.getrandbits(8)
        reset = 1 if r == 0 else 0
        row = {'d': d, 'reset': reset}
        if rng.random() < 0.3:
            mid = {}
            if rng.random() < 0.5:
                mid['d'] = rng.getrandbits(8)
            if rng.random() < 0.5:
                mid['reset'] = rng.choice([0, 1])
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows[:cycles]
