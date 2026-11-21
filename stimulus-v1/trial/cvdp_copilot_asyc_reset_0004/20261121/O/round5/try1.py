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
        elif i < 47:
            reset = 1
        elif i < 90:
            reset = 0
        elif i < 92:
            reset = 1
        elif i < 140:
            reset = 0
        elif i < 142:
            reset = 1
        elif i < 200:
            reset = 0
        else:
            if reset == 1:
                if rng.random() < 0.9:
                    reset = 0
            else:
                if rng.random() < 0.02:
                    reset = 1
        rows.append({'reset': reset})
    return rows
