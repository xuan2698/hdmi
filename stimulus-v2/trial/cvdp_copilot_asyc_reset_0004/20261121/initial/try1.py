def stimulus(rng, cycles):
    rows = []
    reset = 1
    cnt = 31
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i == 3:
            reset = 0
        elif i == 1000:
            reset = 1
        elif i == 1003:
            reset = 0
        elif i == 5000:
            reset = 1
        elif i == 5002:
            reset = 0
        elif i == 12000:
            reset = 1
        elif i == 12001:
            reset = 0
        row = {'reset': reset}
        rows.append(row)
        if reset:
            cnt = 31
        else:
            if cnt > 0:
                cnt = cnt - 1
            else:
                cnt = 0
    return rows
