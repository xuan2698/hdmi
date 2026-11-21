def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 4:
            reset = 1
        elif i < 6:
            reset = 0
        elif i < 40:
            reset = 0
        else:
            r = rng.random()
            if r < 0.015:
                reset = 1
            elif r < 0.05:
                reset = 0
        row = {'reset': reset}
        if i >= 6 and rng.random() < 0.08:
            row['mid'] = {'reset': 1 if rng.random() < 0.5 else 0}
        rows.append(row)
    return rows
