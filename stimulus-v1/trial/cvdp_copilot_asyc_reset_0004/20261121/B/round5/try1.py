def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 6:
            reset = 1
        elif i < 12:
            reset = 0
        elif i < 60:
            reset = 0
        elif i < 80:
            reset = 1 if (i % 11 == 0) else 0
        elif i < 140:
            reset = 0
        elif i < 160:
            reset = 1 if (i % 7 == 0) else 0
        elif i < 220:
            reset = 0
        else:
            if reset == 1:
                if rng.random() < 0.9:
                    reset = 0
            else:
                if rng.random() < 0.012:
                    reset = 1
        rows.append({'reset': reset})
    return rows
