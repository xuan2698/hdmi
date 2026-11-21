def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1, 'in': 0})
    rows.append({'reset': 0, 'in': 0})
    rows.append({'reset': 0, 'in': 1})
    rows.append({'reset': 0, 'in': 0, 'mid': {'in': 1}})
    rows.append({'reset': 0, 'in': 1, 'mid': {'in': 0}})
    rows.append({'reset': 0, 'in': 0})
    rows.append({'reset': 0, 'in': 1})
    rows.append({'reset': 0, 'in': 1})
    rows.append({'reset': 0, 'in': 0})
    rows.append({'reset': 0, 'in': 1, 'mid': {'reset': 1}})
    rows.append({'reset': 1, 'in': 1})
    rows.append({'reset': 0, 'in': 0})
    rows.append({'reset': 0, 'in': 1})
    rows.append({'reset': 0, 'in': 0, 'mid': {'in': 1}})
    rows.append({'reset': 0, 'in': 1})
    rows.append({'reset': 0, 'in': 0})
    while len(rows) < cycles:
        r = {'reset': 0, 'in': rng.getrandbits(1)}
        if rng.randrange(4) == 0:
            r['mid'] = {'in': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
