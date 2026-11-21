def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 4:
            reset = 1
        elif i < 6:
            reset = 0
        else:
            r = rng.random()
            if r < 0.015:
                reset = 1
            elif r < 0.05:
                reset = 0
            elif r < 0.07:
                reset = 1
            else:
                reset = 0
        row = {'reset': reset}
        if rng.random() < 0.05:
            row['mid'] = {'reset': 1 if rng.random() < 0.5 else 0}
        rows.append(row)
    return rows
