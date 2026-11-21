def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i < 6:
            reset = 0
        else:
            if rng.random() < 0.02:
                reset = 1
            elif reset == 1 and rng.random() < 0.7:
                reset = 0
        rows.append({'reset': reset})
    return rows
