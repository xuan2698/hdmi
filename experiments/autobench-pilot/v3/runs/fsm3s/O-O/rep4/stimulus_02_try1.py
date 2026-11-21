def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1, 'in': 0})
    rows.append({'reset': 0, 'in': 0})
    rows.append({'reset': 0, 'in': 1})
    rows.append({'reset': 0, 'in': 1, 'mid': {'in': 0}})
    rows.append({'reset': 0, 'in': 0})
    rows.append({'reset': 0, 'in': 1, 'mid': {'in': 1}})
    rows.append({'reset': 0, 'in': 0, 'mid': {'in': 1}})
    rows.append({'reset': 0, 'in': 1})
    rows.append({'reset': 0, 'in': 0})
    rows.append({'reset': 0, 'in': 1, 'mid': {'reset': 1}})
    rows.append({'reset': 0, 'in': 0})
    rows.append({'reset': 0, 'in': 1})
    rows.append({'reset': 0, 'in': 0, 'mid': {'in': 1}})
    rows.append({'reset': 0, 'in': 1})
    rows.append({'reset': 0, 'in': 0})
    rows.append({'reset': 0, 'in': 1})
    while len(rows) < cycles:
        r = rng.randrange(4)
        if r == 0:
            rows.append({'reset': 1, 'in': rng.getrandbits(1)})
        elif r == 1:
            rows.append({'reset': 0, 'in': rng.getrandbits(1), 'mid': {'in': rng.getrandbits(1)}})
        else:
            rows.append({'reset': 0, 'in': rng.getrandbits(1)})
    return rows[:cycles]
