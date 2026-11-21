def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(4000):
        if i < 3:
            reset = 1
        elif i < 5:
            reset = 0
        elif i < 6:
            reset = 1
        elif i < 8:
            reset = 0
        elif i < 9:
            reset = 1
        elif i < 50:
            reset = 0
        elif i < 52:
            reset = 1
        elif i < 100:
            reset = 0
        elif i < 102:
            reset = 1
        elif i < 300:
            reset = 0
        elif i < 302:
            reset = 1
        elif i < 700:
            reset = 0
        elif i < 702:
            reset = 1
        elif i < 1500:
            reset = 0
        elif i < 1502:
            reset = 1
        elif i < 2500:
            reset = 0
        elif i < 2502:
            reset = 1
        elif i < 3500:
            reset = 0
        elif i < 3502:
            reset = 1
        else:
            reset = 0
        rows.append({'reset': reset})
    return rows
