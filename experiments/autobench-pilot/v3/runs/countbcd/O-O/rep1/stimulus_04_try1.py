def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(10):
        rows.append({'reset': 0})
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(4):
        rows.append({'reset': 0})
    while len(rows) < cycles:
        r = rng.randrange(0, 2)
        rows.append({'reset': r})
    return rows[:cycles]
