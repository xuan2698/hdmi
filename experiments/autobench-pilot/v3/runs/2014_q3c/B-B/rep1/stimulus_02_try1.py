def stimulus(rng, cycles):
    rows = []
    rows.append({'x': 0, 'y': 0})
    rows.append({'x': 1, 'y': 0})
    rows.append({'x': 0, 'y': 1})
    rows.append({'x': 1, 'y': 1})
    rows.append({'x': 0, 'y': 2})
    rows.append({'x': 1, 'y': 2})
    rows.append({'x': 0, 'y': 3})
    rows.append({'x': 1, 'y': 3})
    rows.append({'x': 0, 'y': 4})
    rows.append({'x': 1, 'y': 4})
    rows.append({'x': 0, 'y': 5, 'mid': {'x': 1}})
    rows.append({'x': 1, 'y': 5, 'mid': {'x': 0}})
    rows.append({'x': 0, 'y': 6})
    rows.append({'x': 1, 'y': 6})
    rows.append({'x': 0, 'y': 7})
    rows.append({'x': 1, 'y': 7})
    while len(rows) < cycles:
        y = rng.randrange(8)
        x = rng.getrandbits(1)
        r = {'x': x, 'y': y}
        if rng.random() < 0.3:
            r['mid'] = {'x': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
