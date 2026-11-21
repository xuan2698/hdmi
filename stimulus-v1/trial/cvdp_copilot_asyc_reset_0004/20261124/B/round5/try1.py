def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i < 6:
            reset = 0
        elif i < 45:
            reset = 0
        elif i < 55:
            reset = 1 if (i % 4 == 0) else 0
        elif i < 70:
            reset = 0
        elif i < 80:
            reset = 1 if (i % 2 == 0) else 0
        else:
            r = rng.random()
            if r < 0.02:
                reset = 1
            elif r < 0.05:
                reset = 0
            elif r < 0.06:
                reset = 1 if reset == 0 else 0
        rows.append({'reset': reset})
    return rows
