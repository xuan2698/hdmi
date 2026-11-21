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
        elif i < 250:
            reset = 0
        elif i == 250:
            reset = 1
        elif i < 252:
            reset = 0
        elif i < 600:
            reset = 0
        elif i == 600:
            reset = 1
        elif i < 602:
            reset = 0
        elif i < 1200:
            reset = 0
        elif i == 1200:
            reset = 1
        elif i < 1202:
            reset = 0
        elif i < 2000:
            reset = 0
        elif i == 2000:
            reset = 1
        elif i < 2002:
            reset = 0
        elif i < 3000:
            reset = 0
        elif i == 3000:
            reset = 1
        elif i < 3002:
            reset = 0
        elif i < 3800:
            reset = 0
        elif i == 3800:
            reset = 1
        elif i < 3802:
            reset = 0
        else:
            reset = 0
        rows.append({'reset': reset})
    return rows
