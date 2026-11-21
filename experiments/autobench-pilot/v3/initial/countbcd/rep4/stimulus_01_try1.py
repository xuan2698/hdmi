def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(cycles - 2):
        r = {'reset': 0}
        if i % 17 == 0:
            r['reset'] = 1
        rows.append(r)
    return rows[:cycles]
