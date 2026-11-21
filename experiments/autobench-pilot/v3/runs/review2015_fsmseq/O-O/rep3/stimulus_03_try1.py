def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1, 'data': 0})
    rows.append({'reset': 1, 'data': 1})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 0})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 1, 'mid': {'data': 0}})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 0})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 0})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 1, 'data': 1})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 1})
    while len(rows) < cycles:
        r = rng.randrange(8)
        if r == 0:
            rows.append({'reset': 1, 'data': rng.getrandbits(1)})
        elif r == 1:
            rows.append({'reset': 0, 'data': 1, 'mid': {'data': rng.getrandbits(1)}})
        elif r == 2:
            rows.append({'reset': 0, 'data': 1})
        elif r == 3:
            rows.append({'reset': 0, 'data': 0})
        else:
            rows.append({'reset': 0, 'data': rng.getrandbits(1)})
    return rows[:cycles]
