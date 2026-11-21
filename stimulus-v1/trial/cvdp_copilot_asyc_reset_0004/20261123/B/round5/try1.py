def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i < 6:
            reset = 0
        else:
            if reset == 1:
                if rng.random() < 0.92:
                    reset = 0
            else:
                if rng.random() < 0.02:
                    reset = 1
        rows.append({'reset': reset})
    return rows
