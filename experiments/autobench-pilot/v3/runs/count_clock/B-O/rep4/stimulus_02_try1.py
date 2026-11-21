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
    rows.append({'reset': 1, 'ena': 1, 'mid': {'ena': 0}})
    rows.append({'reset': 0, 'ena': 0, 'mid': {'reset': 1}})
    rows.append({'reset': 0, 'ena': 1})
    rows.append({'reset': 0, 'ena': 1})
    while len(rows) < cycles:
        r = rng.randrange(100)
        if r < 8:
            rows.append({'reset': 1, 'ena': rng.getrandbits(1)})
        elif r < 20:
            rows.append({'reset': 0, 'ena': 0})
        elif r < 35:
            rows.append({'reset': 0, 'ena': 1, 'mid': {'ena': 0}})
        elif r < 50:
            rows.append({'reset': 0, 'ena': 0, 'mid': {'ena': 1}})
        elif r < 60:
            rows.append({'reset': 1, 'ena': rng.getrandbits(1), 'mid': {'reset': 0}})
        else:
            rows.append({'reset': 0, 'ena': 1})
    return rows[:cycles]
