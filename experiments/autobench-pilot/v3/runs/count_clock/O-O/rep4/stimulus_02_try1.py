def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1, 'ena': 0})
    rows.append({'reset': 1, 'ena': 1})
    rows.append({'reset': 0, 'ena': 0})
    rows.append({'reset': 0, 'ena': 1})
    rows.append({'reset': 0, 'ena': 1, 'mid': {'ena': 0}})
    rows.append({'reset': 0, 'ena': 0, 'mid': {'ena': 1}})
    rows.append({'reset': 1, 'ena': 0, 'mid': {'reset': 0}})
    rows.append({'reset': 0, 'ena': 1, 'mid': {'reset': 1}})
    rows.append({'reset': 1, 'ena': 1, 'mid': {'reset': 0, 'ena': 0}})
    rows.append({'reset': 0, 'ena': 0, 'mid': {'reset': 1, 'ena': 1}})
    rows.append({'reset': 0, 'ena': 1})
    rows.append({'reset': 0, 'ena': 1})
    rows.append({'reset': 0, 'ena': 1})
    rows.append({'reset': 0, 'ena': 1})
    rows.append({'reset': 0, 'ena': 1})
    rows.append({'reset': 0, 'ena': 1})
    while len(rows) < cycles:
        r = rng.randrange(100)
        if r < 8:
            row = {'reset': 1, 'ena': rng.getrandbits(1)}
        elif r < 20:
            row = {'reset': 0, 'ena': 0}
        else:
            row = {'reset': 0, 'ena': 1}
        if rng.randrange(4) == 0:
            mid = {}
            if rng.randrange(2):
                mid['reset'] = rng.getrandbits(1)
            if rng.randrange(2):
                mid['ena'] = rng.getrandbits(1)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows[:cycles]
