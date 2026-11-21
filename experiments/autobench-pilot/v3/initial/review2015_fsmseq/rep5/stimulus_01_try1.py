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
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 0})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 1, 'data': 0})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 0})
    rows.append({'reset': 0, 'data': 1})
    while len(rows) < cycles:
        r = rng.randrange(10)
        if r < 3:
            rows.append({'reset': 0, 'data': rng.getrandbits(1)})
        elif r < 6:
            seq = [1, 1, 0, 1]
            for b in seq:
                if len(rows) < cycles:
                    rows.append({'reset': 0, 'data': b})
        elif r < 8:
            rows.append({'reset': 0, 'data': rng.choice([0, 1]), 'mid': {'data': rng.getrandbits(1)}})
        else:
            rows.append({'reset': rng.getrandbits(1), 'data': rng.getrandbits(1)})
    return rows[:cycles]
