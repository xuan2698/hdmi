def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(4000):
        if i < 2:
            reset = 1
        elif i < 4:
            reset = 0
        elif i == 4:
            reset = 1
        elif i < 7:
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
        elif i < 200:
            reset = 0
        elif i < 202:
            reset = 1
        elif i < 400:
            reset = 0
        elif i < 402:
            reset = 1
        elif i < 800:
            reset = 0
        elif i < 802:
            reset = 1
        elif i < 1600:
            reset = 0
        elif i < 1602:
            reset = 1
        elif i < 2400:
            reset = 0
        elif i < 2402:
            reset = 1
        elif i < 3200:
            reset = 0
        elif i < 3202:
            reset = 1
        else:
            reset = 0
        rows.append({'reset': reset})
    return rows
