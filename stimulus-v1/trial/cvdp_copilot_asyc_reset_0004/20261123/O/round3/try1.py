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
            if reset == 1:
                if rng.random() < 0.7:
                    reset = 0
            else:
                if rng.random() < 0.012:
                    reset = 1
        rows.append({'reset': reset})
    return rows
