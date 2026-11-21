def stimulus(rng, cycles):
    rows = []
    reset = 1
    cnt = 31
    for i in range(cycles):
        if i < 2:
            reset = 1
        elif i < 4:
            reset = 0
        elif i < 6:
            reset = 1
        else:
            reset = 0
        if i == 50:
            reset = 1
        if i == 52:
            reset = 0
        if i == 100:
            reset = 1
        if i == 101:
            reset = 0
        if i == 200:
            reset = 1
        if i == 203:
            reset = 0
        if i == 500:
            reset = 1
        if i == 501:
            reset = 0
        if i == 1000:
            reset = 1
        if i == 1002:
            reset = 0
        if i == 2000:
            reset = 1
        if i == 2001:
            reset = 0
        if i == 3000:
            reset = 1
        if i == 3003:
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
