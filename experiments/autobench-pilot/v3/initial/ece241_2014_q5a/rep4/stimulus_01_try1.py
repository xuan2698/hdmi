def stimulus(rng, cycles):
    rows = []
    rows.append({'areset': 1, 'x': 0})
    rows.append({'areset': 1, 'x': 1})
    rows.append({'areset': 0, 'x': 0})
    rows.append({'areset': 0, 'x': 1})
    rows.append({'areset': 0, 'x': 0, 'mid': {'x': 1}})
    rows.append({'areset': 0, 'x': 1, 'mid': {'x': 0}})
    rows.append({'areset': 1, 'x': 0, 'mid': {'areset': 0}})
    rows.append({'areset': 0, 'x': 1})
    rows.append({'areset': 0, 'x': 0})
    rows.append({'areset': 0, 'x': 1})
    rows.append({'areset': 0, 'x': 1})
    rows.append({'areset': 0, 'x': 0})
    rows.append({'areset': 1, 'x': 1})
    rows.append({'areset': 0, 'x': 0})
    rows.append({'areset': 0, 'x': 1})
    rows.append({'areset': 0, 'x': 0})
    while len(rows) < cycles:
        r = rng.randrange(4)
        if r == 0:
            rows.append({'areset': 1, 'x': rng.getrandbits(1)})
        elif r == 1:
            rows.append({'areset': 0, 'x': rng.getrandbits(1), 'mid': {'x': rng.getrandbits(1)}})
        elif r == 2:
            rows.append({'areset': 0, 'x': rng.getrandbits(1), 'mid': {'areset': rng.getrandbits(1)}})
        else:
            rows.append({'areset': 0, 'x': rng.getrandbits(1)})
    return rows[:cycles]
