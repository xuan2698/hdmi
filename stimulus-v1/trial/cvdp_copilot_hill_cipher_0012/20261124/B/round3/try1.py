def stimulus(rng, cycles):
    rows = []
    reset = 1
    start = 0
    plaintext = 0
    key = 0
    for i in range(cycles):
        if i < 3:
            reset = 1
            start = 0
            plaintext = 0
            key = 0
        elif i < 5:
            reset = 0
            start = 0
        else:
            reset = 0
            if i % 7 == 6:
                start = 1
            else:
                start = 0
            if i % 11 == 0:
                plaintext = rng.randrange(0, 1 << 15)
                key = rng.randrange(0, 1 << 45)
            elif i % 5 == 0:
                plaintext = rng.randrange(0, 1 << 15)
            elif i % 6 == 0:
                key = rng.randrange(0, 1 << 45)
            if i % 23 == 15:
                reset = 1
                start = 0
        row = {
            'reset': reset,
            'start': start,
            'plaintext': plaintext,
            'key': key,
        }
        if i % 13 == 6:
            row['mid'] = {'start': 0}
        elif i % 17 == 11:
            row['mid'] = {'start': 1}
        rows.append(row)
    return rows
