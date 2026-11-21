def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(14):
        rows.append({'reset': 0})
    while len(rows) < cycles:
        r = rng.random()
        if r < 0.1:
            rows.append({'reset': 1})
        elif r < 0.2:
            rows.append({'reset': 0, 'mid': {'reset': 1}})
        else:
            rows.append({'reset': 0})
    return rows[:cycles]
