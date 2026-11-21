def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(10):
        rows.append({'reset': 0})
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    while len(rows) < cycles:
        r = rng.randrange(4)
        if r == 0:
            rows.append({'reset': 1})
        else:
            rows.append({'reset': 0})
    return rows[:cycles]
