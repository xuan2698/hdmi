def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 2:
            reset = 1
        elif i < 4:
            reset = 0
        elif i < 6:
            reset = 1
        elif i < 40:
            reset = 0
        else:
            if rng.random() < 0.03:
                reset = 1
            elif rng.random() < 0.2:
                reset = 0
        rows.append({'reset': reset})
    return rows
