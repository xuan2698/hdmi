def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 2:
            reset = 1
        elif i < 40:
            reset = 0
        elif i < 42:
            reset = 1
        elif i < 80:
            reset = 0
        elif i < 81:
            reset = 1
        elif i < 120:
            reset = 0
        elif i < 122:
            reset = 1
        elif i < 200:
            reset = 0
        elif i < 201:
            reset = 1
        elif i < 260:
            reset = 0
        elif i < 262:
            reset = 1
        elif i < 400:
            reset = 0
        elif i < 402:
            reset = 1
        elif i < 600:
            reset = 0
        elif i < 601:
            reset = 1
        elif i < 900:
            reset = 0
        elif i < 902:
            reset = 1
        elif i < 1500:
            reset = 0
        elif i < 1501:
            reset = 1
        elif i < 2500:
            reset = 0
        elif i < 2502:
            reset = 1
        else:
            reset = 0
        rows.append({'reset': reset})
    return rows
