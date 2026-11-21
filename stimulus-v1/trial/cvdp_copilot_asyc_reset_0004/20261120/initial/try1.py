def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i < 5:
            reset = 0
        else:
            if rng.random() < 0.02:
                reset = 1
            elif rng.random() < 0.3:
                reset = 0
        row = {'reset': reset}
        if rng.random() < 0.1:
            row['mid'] = {'reset': 1 if rng.random() < 0.5 else 0}
        rows.append(row)
    return rows
