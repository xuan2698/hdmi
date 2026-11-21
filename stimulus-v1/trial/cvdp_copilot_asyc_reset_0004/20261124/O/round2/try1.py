def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 4:
            reset = 1
        elif i < 8:
            reset = 0
        else:
            if rng.random() < 0.015:
                reset = 1
            elif rng.random() < 0.12:
                reset = 0
        rows.append({'reset': reset})
    return rows
