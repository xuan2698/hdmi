def stimulus(rng, cycles):
    rows = []
    q = 0
    for i in range(cycles):
        reset = 1 if i < 2 else 0
        row = {'reset': reset}
        if i >= 2 and i % 7 == 0:
            row['mid'] = {'reset': 1}
        rows.append(row)
    return rows[:cycles]
