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
    rows.append({'d': 0x34, 'reset': 0, 'mid': {'d': 0x34}})
    rows.append({'d': 0x00, 'reset': 1, 'mid': {'d': 0xFF}})
    rows.append({'d': 0xFF, 'reset': 1, 'mid': {'d': 0x00}})
    rows.append({'d': 0x81, 'reset': 0, 'mid': {'d': 0x18}})
    rows.append({'d': 0x18, 'reset': 0, 'mid': {'d': 0x81}})
    rows.append({'d': 0x7E, 'reset': 0, 'mid': {'d': 0xE7}})
    while len(rows) < cycles:
        r = rng.randrange(4)
        d = rng.getrandbits(8)
        reset = 1 if r == 0 else 0
        row = {'d': d, 'reset': reset}
        if rng.randrange(3) == 0:
            mid = {}
            if rng.randrange(2):
                mid['d'] = rng.getrandbits(8)
            if rng.randrange(2):
                mid['reset'] = rng.randrange(2)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows[:cycles]
