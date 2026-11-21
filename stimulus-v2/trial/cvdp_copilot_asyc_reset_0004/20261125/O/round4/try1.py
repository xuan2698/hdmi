def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i == 3:
            reset = 0
        elif i == 15000:
            reset = 1
        elif i == 15003:
            reset = 0
        elif i == 25000:
            reset = 1
        elif i == 25002:
            reset = 0
        elif i == 35000:
            reset = 1
        elif i == 35001:
            reset = 0
        elif i > 35001 and i < 35010:
            reset = 1 if (i % 2 == 0) else 0
        elif i >= 35010 and i < 36000:
            reset = 0
        elif i >= 36000 and i < 36005:
            reset = 1
        elif i >= 36005 and i < 37000:
            reset = 0
        elif i >= 37000 and i < 37002:
            reset = 1
        elif i >= 37002:
            reset = 0
        row = {'reset': reset}
        rows.append(row)
    return rows
