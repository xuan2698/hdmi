def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 2:
            reset = 1
        elif i < 4:
            reset = 0
        elif i == 4:
            reset = 1
        elif i < 7:
            reset = 0
        elif i == 7:
            reset = 1
        elif i < 10:
            reset = 0
        elif i == 10:
            reset = 1
        elif i < 40:
            reset = 0
        elif i == 40:
            reset = 1
        elif i < 45:
            reset = 0
        elif i == 45:
            reset = 1
        elif i < 100:
            reset = 0
        elif i == 100:
            reset = 1
        elif i < 200:
            reset = 0
        elif i == 200:
            reset = 1
        elif i < 500:
            reset = 0
        elif i == 500:
            reset = 1
        elif i < 1000:
            reset = 0
        elif i == 1000:
            reset = 1
        elif i < 2000:
            reset = 0
        elif i == 2000:
            reset = 1
        elif i < 3000:
            reset = 0
        elif i == 3000:
            reset = 1
        else:
            reset = 0
        row = {'reset': reset}
        if i in (4, 7, 10, 40, 45, 100, 200, 500, 1000, 2000, 3000):
            row['mid'] = {'reset': 0}
        rows.append(row)
    return rows
