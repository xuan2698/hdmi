def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i == 0:
            reset = 1
        elif i == 3:
            reset = 0
        elif i == 5000:
            reset = 1
        elif i == 5003:
            reset = 0
        elif i == 12000:
            reset = 1
        elif i == 12002:
            reset = 0
        elif i == 20000:
            reset = 1
        elif i == 20001:
            reset = 0
        elif i == 30000:
            reset = 1
        elif i == 30004:
            reset = 0
        elif i == 35000:
            reset = 1
        elif i == 35001:
            reset = 0
        elif i == 37000:
            reset = 1
        elif i == 37002:
            reset = 0
        rows.append({'reset': reset})
    return rows
