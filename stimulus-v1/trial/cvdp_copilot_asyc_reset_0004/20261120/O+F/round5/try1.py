def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i < 5:
            reset = 0
        elif i < 40:
            reset = 0
        elif i < 60:
            reset = 0 if rng.random() < 0.8 else 1
        else:
            r = rng.random()
            if r < 0.02:
                reset = 1
            elif r < 0.06:
                reset = 0
        row = {'reset': reset}
        if i >= 5 and rng.random() < 0.04:
            row['mid'] = {'reset': 1 if rng.random() < 0.5 else 0}
        rows.append(row)
    return rows
