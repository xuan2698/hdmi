def stimulus(rng, cycles):
    rows = []
    seq = [1, 1, 0, 1]
    rows.append({'reset': 1, 'data': 0})
    rows.append({'reset': 1, 'data': 1})
    rows.append({'reset': 0, 'data': 0})
    for i in range(4):
        rows.append({'reset': 0, 'data': seq[i]})
    rows.append({'reset': 0, 'data': 1, 'mid': {'data': 0}})
    rows.append({'reset': 0, 'data': 1, 'mid': {'reset': 1}})
    rows.append({'reset': 1, 'data': 1, 'mid': {'data': 0}})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 0})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 1})
    rows.append({'reset': 0, 'data': 0})
    rows.append({'reset': 0, 'data': 1})
    while len(rows) < cycles:
        r = rng.randrange(2)
        d = rng.getrandbits(1)
        row = {'reset': r, 'data': d}
        if rng.random() < 0.3:
            row['mid'] = {'data': rng.getrandbits(1)}
        rows.append(row)
    return rows[:cycles]
