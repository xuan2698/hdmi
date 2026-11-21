def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i < 5:
            reset = 0
        elif i < 7:
            reset = 1
        elif i < 45:
            reset = 0
        else:
            r = rng.random()
            if r < 0.02:
                reset = 1
            elif r < 0.15:
                reset = 0
        rows.append({'reset': reset})
    return rows
