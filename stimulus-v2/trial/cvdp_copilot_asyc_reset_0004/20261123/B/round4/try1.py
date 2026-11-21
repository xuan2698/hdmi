def stimulus(rng, cycles):
    rows = []
    reset = 1
    cnt = 31
    for i in range(cycles):
        if i < 2:
            reset = 1
        elif i < 4:
            reset = 0
        else:
            reset = 0
        if i == 4:
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
        if i == 100:
            reset = 1
        if i == 102:
            reset = 0
        if i == 102:
            cnt = 31
        if i == 200:
            reset = 1
        if i == 201:
            reset = 0
        if i == 201:
            cnt = 31
        if i == 500:
            reset = 1
        if i == 503:
            reset = 0
        if i == 503:
            cnt = 31
        if i == 1000:
            reset = 1
        if i == 1001:
            reset = 0
        if i == 1001:
            cnt = 31
        if i == 2000:
            reset = 1
        if i == 2002:
            reset = 0
        if i == 2002:
            cnt = 31
        if i == 3000:
            reset = 1
        if i == 3001:
            reset = 0
        if i == 3001:
            cnt = 31
    return rows
