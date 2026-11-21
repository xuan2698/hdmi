def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 4:
            reset = 1
        elif i < 6:
            reset = 0
        elif i < 9:
            reset = 1
        elif i < 13:
            reset = 0
        elif i < 70:
            reset = 0
        else:
            r = rng.random()
            if r < 0.015:
                reset = 1
            elif r < 0.12:
                reset = 0
        rows.append({'reset': reset})
    return rows
