def stimulus(rng, cycles):
    rows = []
    rows.append({'d': 0, 'r': 1})
    rows.append({'d': 1, 'r': 1})
    rows.append({'d': 1, 'r': 0})
    rows.append({'d': 0, 'r': 0})
    rows.append({'d': 1, 'r': 0, 'mid': {'d': 0}})
    rows.append({'d': 0, 'r': 0, 'mid': {'d': 1}})
    rows.append({'d': 1, 'r': 1, 'mid': {'r': 0}})
    rows.append({'d': 0, 'r': 1, 'mid': {'r': 0}})
    rows.append({'d': 1, 'r': 0, 'mid': {'r': 1}})
    rows.append({'d': 0, 'r': 0, 'mid': {'r': 1}})
    rows.append({'d': 1, 'r': 1, 'mid': {'d': 0, 'r': 0}})
    rows.append({'d': 0, 'r': 1, 'mid': {'d': 1, 'r': 0}})
    while len(rows) < cycles:
        d = rng.getrandbits(1)
        r = rng.getrandbits(1)
        row = {'d': d, 'r': r}
        if rng.random() < 0.4:
            mid = {}
            if rng.random() < 0.5:
                mid['d'] = rng.getrandbits(1)
            if rng.random() < 0.5:
                mid['r'] = rng.getrandbits(1)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows[:cycles]
