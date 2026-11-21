def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 8:
            reset = 1
        elif i < 12:
            reset = 0
        elif i < 60:
            reset = 0
        elif i < 64:
            reset = 1
        elif i < 130:
            reset = 0
        elif i < 134:
            reset = 1
        elif i < 200:
            reset = 0
        else:
            r = rng.random()
            if r < 0.015:
                reset = 1
            elif r < 0.08:
                reset = 0
            elif r < 0.12:
                reset = 1 if reset == 0 else 0
        rows.append({'reset': reset})
    return rows
