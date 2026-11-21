def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i < 6:
            reset = 0
        elif i < 40:
            reset = 0
        elif i < 42:
            reset = 1
        elif i < 100:
            reset = 0
        elif i < 102:
            reset = 1
        elif i < 160:
            reset = 0
        elif i < 163:
            reset = 1
        elif i < 220:
            reset = 0
        elif i < 222:
            reset = 1
        elif i < 300:
            reset = 0
        elif i < 302:
            reset = 1
        elif i < 380:
            reset = 0
        else:
            if reset == 1:
                if rng.random() < 0.90:
                    reset = 0
            else:
                if rng.random() < 0.02:
                    reset = 1
        rows.append({'reset': reset})
    return rows
