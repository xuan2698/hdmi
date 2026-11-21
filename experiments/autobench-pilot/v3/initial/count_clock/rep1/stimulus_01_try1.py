def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1, 'ena': 0})
    rows.append({'reset': 1, 'ena': 1})
    rows.append({'reset': 0, 'ena': 0})
    rows.append({'reset': 0, 'ena': 1})
    for i in range(cycles - 4):
        r = 1 if rng.randrange(100) < 3 else 0
        e = 1 if rng.randrange(100) < 70 else 0
        row = {'reset': r, 'ena': e}
        if rng.randrange(100) < 15:
            row['mid'] = {'ena': 1 - e}
        rows.append(row)
    return rows[:cycles]
