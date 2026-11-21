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
            plaintext = 0
            key = 0
        else:
            reset = 0
            if i % 8 == 5:
                start = 1
            else:
                start = 0
            if i % 19 == 0:
                plaintext = rng.randrange(0, 1 << 15)
                key = rng.randrange(0, 1 << 45)
            elif i % 13 == 0:
                plaintext = rng.randrange(0, 1 << 15)
            elif i % 11 == 0:
                key = rng.randrange(0, 1 << 45)
            elif i % 29 == 0:
                plaintext = 0
                key = 0
            elif i % 31 == 0:
                plaintext = (1 << 15) - 1
                key = (1 << 45) - 1
            elif i % 7 == 0:
                plaintext = rng.randrange(0, 1 << 15)
                key = rng.randrange(0, 1 << 45)
        row = {
            'reset': reset,
            'start': start,
            'plaintext': plaintext,
            'key': key,
        }
        if i % 10 == 7:
            row['mid'] = {'start': 0}
        rows.append(row)
    return rows
