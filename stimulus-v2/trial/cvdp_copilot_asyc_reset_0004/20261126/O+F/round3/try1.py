def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(4000):
        if i < 3:
            reset = 1
        elif i < 5:
            reset = 0
        elif i == 5:
            reset = 1
        elif i < 7:
            reset = 0
        elif i == 7:
            reset = 1
        elif i < 9:
            reset = 0
        elif i < 50:
            reset = 0
        elif i == 50:
            reset = 1
        elif i < 52:
            reset = 0
        elif i == 52:
            reset = 1
        elif i < 54:
            reset = 0
        elif i < 120:
            reset = 0
        elif i == 120:
            reset = 1
        elif i < 122:
            reset = 0
        elif i < 300:
            reset = 0
        elif i == 300:
            reset = 1
        elif i < 302:
            reset = 0
        elif i < 700:
            reset = 0
        elif i == 700:
            reset = 1
        elif i < 702:
            reset = 0
        elif i < 1500:
            reset = 0
        elif i == 1500:
            reset = 1
        elif i < 1502:
            reset = 0
        elif i < 2500:
            reset = 0
        elif i == 2500:
            reset = 1
        elif i < 2502:
            reset = 0
        elif i < 3500:
            reset = 0
        elif i == 3500:
            reset = 1
        elif i < 3502:
            reset = 0
        else:
            reset = 0
        rows.append({'reset': reset})
    return rows
