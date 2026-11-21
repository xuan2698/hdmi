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
        elif i < 80:
            reset = 0
        elif i < 82:
            reset = 1
        elif i < 120:
            reset = 0
        elif i < 122:
            reset = 1
        elif i < 160:
            reset = 0
        elif i < 162:
            reset = 1
        elif i < 200:
            reset = 0
        elif i < 202:
            reset = 1
        elif i < 240:
            reset = 0
        elif i < 242:
            reset = 1
        elif i < 280:
            reset = 0
        elif i < 282:
            reset = 1
        elif i < 320:
            reset = 0
        elif i < 322:
            reset = 1
        elif i < 360:
            reset = 0
        elif i < 362:
            reset = 1
        elif i < 400:
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
