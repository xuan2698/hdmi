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
        elif i < 6:
            reset = 0
        elif i == 6:
            reset = 1
        elif i < 8:
            reset = 0
        elif i < 40:
            reset = 0
        elif i == 40:
            reset = 1
        elif i < 42:
            reset = 0
        elif i == 42:
            reset = 1
        elif i < 44:
            reset = 0
        elif i < 100:
            reset = 0
        elif i == 100:
            reset = 1
        elif i < 102:
            reset = 0
        elif i < 200:
            reset = 0
        elif i == 200:
            reset = 1
        elif i < 202:
            reset = 0
        elif i < 400:
            reset = 0
        elif i == 400:
            reset = 1
        elif i < 402:
            reset = 0
        elif i < 800:
            reset = 0
        elif i == 800:
            reset = 1
        elif i < 802:
            reset = 0
        elif i < 1600:
            reset = 0
        elif i == 1600:
            reset = 1
        elif i < 1602:
            reset = 0
        elif i < 3200:
            reset = 0
        elif i == 3200:
            reset = 1
        elif i < 3202:
            reset = 0
        else:
            reset = 0
        rows.append({'reset': reset})
    return rows
