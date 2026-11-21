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
        r = rng.randrange(4)
        if r == 0:
            rows.append({'reset': 1, 'ena': rng.getrandbits(1)})
        elif r == 1:
            rows.append({'reset': 0, 'ena': 0})
        elif r == 2:
            rows.append({'reset': 0, 'ena': 1, 'mid': {'ena': rng.getrandbits(1)}})
        else:
            rows.append({'reset': rng.getrandbits(1), 'ena': 1})
    return rows[:cycles]
