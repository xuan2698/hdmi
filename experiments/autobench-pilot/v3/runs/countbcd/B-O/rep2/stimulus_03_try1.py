def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(cycles - 2):
        r = {'reset': 0}
        if i % 7 == 0:
            r['reset'] = 1
        elif i % 5 == 0:
            r['reset'] = rng.getrandbits(1)
        rows.append(r)
    return rows[:cycles]
