def stimulus(rng, cycles):
    rows = []
    rows.append({'d': 0, 'reset': 1})
    rows.append({'d': 255, 'reset': 1})
    rows.append({'d': 0, 'reset': 0})
    rows.append({'d': 255, 'reset': 0})
    rows.append({'d': 170, 'reset': 0})
    rows.append({'d': 85, 'reset': 0})
    rows.append({'d': 1, 'reset': 0})
    rows.append({'d': 128, 'reset': 0})
    rows.append({'d': 0, 'reset': 1, 'mid': {'reset': 0}})
    rows.append({'d': 255, 'reset': 0, 'mid': {'d': 0}})
    rows.append({'d': 0, 'reset': 0, 'mid': {'d': 255}})
    rows.append({'d': 170, 'reset': 1, 'mid': {'reset': 0, 'd': 85}})
    rows.append({'d': 85, 'reset': 0, 'mid': {'d': 170}})
    rows.append({'d': 1, 'reset': 0, 'mid': {'reset': 1}})
    rows.append({'d': 128, 'reset': 1, 'mid': {'reset': 0}})
    rows.append({'d': 0, 'reset': 0, 'mid': {'d': 255, 'reset': 1}})
    while len(rows) < cycles:
        r = rng.randrange(4)
        d = rng.getrandbits(8)
        reset = 1 if r == 0 else 0
        row = {'d': d, 'reset': reset}
        if rng.random() < 0.4:
            mid = {}
            if rng.random() < 0.5:
                mid['d'] = rng.getrandbits(8)
            if rng.random() < 0.5:
                mid['reset'] = rng.choice([0, 1])
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows[:cycles]
