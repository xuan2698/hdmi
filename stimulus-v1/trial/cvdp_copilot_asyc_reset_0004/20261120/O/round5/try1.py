def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i < 5:
            reset = 0
        elif i < 45:
            reset = 0
        elif i < 48:
            reset = 1
        elif i < 90:
            reset = 0
        elif i < 93:
            reset = 1
        elif i < 140:
            reset = 0
        elif i < 143:
            reset = 1
        elif i < 200:
            reset = 0
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
