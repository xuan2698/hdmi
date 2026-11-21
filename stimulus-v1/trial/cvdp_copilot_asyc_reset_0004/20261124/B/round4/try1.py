def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 4:
            reset = 1
        elif i < 8:
            reset = 0
        elif i < 50:
            reset = 0
        elif i < 60:
            reset = 1 if (i % 3 == 0) else 0
        else:
            r = rng.random()
            if r < 0.015:
                reset = 1
            elif r < 0.03:
                reset = 0
            elif r < 0.04:
                reset = 1 if reset == 0 else 0
        rows.append({'reset': reset})
    return rows
