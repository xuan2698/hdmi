def stimulus(rng, cycles):
    rows = []
    reset = 1
    start = 0
    plaintext = 0
    key = 0
    for i in range(cycles):
        if i < 4:
            reset = 1
            start = 0
            plaintext = 0
            key = 0
        elif i < 6:
            reset = 0
            start = 0
            plaintext = 0
            key = 0
        else:
            reset = 0
            if i % 7 == 0:
                start = 1
            else:
                start = 0
            if i % 11 == 0:
                plaintext = rng.randrange(0, 1 << 15)
                key = rng.randrange(0, 1 << 45)
            elif i % 5 == 0:
                plaintext = rng.randrange(0, 1 << 15)
            elif i % 3 == 0:
                key = rng.randrange(0, 1 << 45)
            elif i % 23 == 0:
                plaintext = 0
                key = 0
            elif i % 27 == 0:
                plaintext = (1 << 15) - 1
                key = (1 << 45) - 1
            elif i % 19 == 0:
                plaintext = rng.randrange(0, 1 << 15)
                key = (1 << 45) - 1
        row = {
            'reset': reset,
            'start': start,
            'plaintext': plaintext,
            'key': key,
        }
        if i % 9 == 4:
            row['mid'] = {'start': 0}
        elif i % 13 == 6:
            row['mid'] = {'plaintext': rng.randrange(0, 1 << 15)}
        elif i % 17 == 8:
            row['mid'] = {'key': rng.randrange(0, 1 << 45)}
        elif i % 25 == 12:
            row['mid'] = {'start': 1}
        rows.append(row)
    return rows
