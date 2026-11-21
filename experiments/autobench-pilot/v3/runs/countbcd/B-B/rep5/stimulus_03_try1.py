def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(cycles - 2):
        r = {'reset': 0}
        if i % 7 == 0:
            r['reset'] = 1
        if i % 11 == 0:
            r['mid'] = {'reset': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
