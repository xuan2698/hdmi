def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 4:
            reset = 1
        elif i < 8:
            reset = 0
        elif i < 40:
            reset = 0
        elif i < 44:
            reset = 1
        elif i < 80:
            reset = 0
        else:
            if reset == 1:
                if rng.random() < 0.6:
                    reset = 0
            else:
                if rng.random() < 0.015:
                    reset = 1
        rows.append({'reset': reset})
    return rows
