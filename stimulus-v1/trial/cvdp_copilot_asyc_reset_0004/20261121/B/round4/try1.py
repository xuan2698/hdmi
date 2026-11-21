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
        elif i < 70:
            reset = 1 if (i % 9 == 0) else 0
        elif i < 120:
            reset = 0
        else:
            if reset == 1:
                if rng.random() < 0.85:
                    reset = 0
            else:
                if rng.random() < 0.015:
                    reset = 1
        rows.append({'reset': reset})
    return rows
