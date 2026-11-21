def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i < 5:
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
            if reset == 1:
                if rng.random() < 0.9:
                    reset = 0
            else:
                if rng.random() < 0.02:
                    reset = 1
        rows.append({'reset': reset})
    return rows
