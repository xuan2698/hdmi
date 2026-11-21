def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i < 6:
            reset = 0
        elif i < 50:
            reset = 0
        elif i < 53:
            reset = 1
        elif i < 100:
            reset = 0
        elif i < 103:
            reset = 1
        elif i < 150:
            reset = 0
        else:
            if reset == 1:
                if rng.random() < 0.85:
                    reset = 0
            else:
                if rng.random() < 0.02:
                    reset = 1
        rows.append({'reset': reset})
    return rows
