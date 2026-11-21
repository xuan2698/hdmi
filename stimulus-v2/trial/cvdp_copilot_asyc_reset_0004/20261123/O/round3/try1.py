def stimulus(rng, cycles):
    rows = []
    reset = 1
    cnt = 31
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i < 5:
            reset = 0
        else:
            reset = 0
        if i == 5:
            cnt = 31
        row = {'reset': reset}
        rows.append(row)
        if reset:
            cnt = 31
        else:
            if cnt > 0:
                cnt = cnt - 1
            else:
                cnt = 0
        if i >= 5 and i < 40:
            pass
        if i == 40:
            reset = 1
        if i == 42:
            reset = 0
        if i == 42:
            cnt = 31
    return rows
