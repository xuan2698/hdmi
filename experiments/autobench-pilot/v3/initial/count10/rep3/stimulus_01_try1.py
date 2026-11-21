def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(cycles - 2):
        r = 0
        if i % 10 == 0 and i > 0:
            r = 1
        elif rng.random() < 0.1:
            r = 1
        row = {'reset': r}
        if rng.random() < 0.3:
            row['mid'] = {'reset': rng.getrandbits(1)}
        rows.append(row)
    return rows[:cycles]
