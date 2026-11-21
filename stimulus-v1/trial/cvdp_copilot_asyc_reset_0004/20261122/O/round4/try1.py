def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 4:
            reset = 1
        elif i < 8:
            reset = 0
        elif i < 60:
            reset = 0
        elif i < 63:
            reset = 1
        elif i < 120:
            reset = 0
        elif i < 122:
            reset = 1
        elif i < 180:
            reset = 0
        elif i < 183:
            reset = 1
        elif i < 260:
            reset = 0
        elif i < 262:
            reset = 1
        elif i < 340:
            reset = 0
        else:
            if reset == 1:
                if rng.random() < 0.92:
                    reset = 0
            else:
                if rng.random() < 0.015:
                    reset = 1
        rows.append({'reset': reset})
    return rows
