def stimulus(rng, cycles):
    rows = []
    reset = 1
    cnt = 31
    for i in range(cycles):
        if i < 2:
            reset = 1
        elif i == 2:
            reset = 0
        elif i == 40:
            reset = 1
        elif i == 41:
            reset = 0
        elif i == 200:
            reset = 1
        elif i == 202:
            reset = 0
        elif i == 1500:
            reset = 1
        elif i == 1501:
            reset = 0
        elif i == 3000:
            reset = 1
        elif i == 3003:
            reset = 0
        elif i > 3003 and (i % 500) == 0:
            reset = 1
        elif i > 3003 and (i % 500) == 1:
            reset = 0
        row = {'reset': reset}
        rows.append(row)
        if reset:
            cnt = 31
        else:
            if cnt > 0:
                cnt = (cnt - 1) & 0x1F
            else:
                cnt = 0
    return rows
