def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 4:
            reset = 1
        elif i < 40:
            reset = 0
        elif i < 43:
            reset = 1
        elif i < 80:
            reset = 0
        elif i < 82:
            reset = 1
        elif i < 120:
            reset = 0
        elif i < 123:
            reset = 1
        elif i < 200:
            reset = 0
        else:
            if reset == 1:
                if rng.random() < 0.9:
                    reset = 0
            else:
                if rng.random() < 0.015:
                    reset = 1
        rows.append({'reset': reset})
    return rows
