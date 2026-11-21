def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 6:
            reset = 1
        elif i < 10:
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
            elif r < 0.10:
                reset = 0
            elif r < 0.14:
                reset = 1 if reset == 0 else 0
        rows.append({'reset': reset})
    return rows
