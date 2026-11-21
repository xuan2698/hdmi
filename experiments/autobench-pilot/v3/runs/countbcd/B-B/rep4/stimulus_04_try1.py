def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(10):
        rows.append({'reset': 0})
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(cycles - len(rows)):
        r = {'reset': 0}
        if rng.random() < 0.05:
            r['reset'] = 1
        rows.append(r)
    return rows[:cycles]
