def stimulus(rng, cycles):
    rows = []
    reset = 1
    start = 0
    plaintext = 0
    key = 0
    for i in range(cycles):
        if i < 5:
            reset = 1
            start = 0
            plaintext = 0
            key = 0
        elif i < 10:
            reset = 0
            start = 0
            plaintext = rng.randrange(0, 1 << 15)
            key = rng.randrange(0, 1 << 45)
        else:
            reset = 0
            phase = (i - 10) % 14
            if phase == 0:
                start = 1
                plaintext = rng.randrange(0, 1 << 15)
                key = rng.randrange(0, 1 << 45)
            elif phase == 1:
                start = 0
            elif phase == 2:
                start = 0
                if rng.random() < 0.5:
                    plaintext = rng.randrange(0, 1 << 15)
            elif phase == 3:
                start = 0
                if rng.random() < 0.4:
                    key = rng.randrange(0, 1 << 45)
            elif phase == 4:
                start = 0
                if rng.random() < 0.3:
                    plaintext = rng.randrange(0, 1 << 15)
                    key = rng.randrange(0, 1 << 45)
            elif phase == 5:
                start = 0
            elif phase == 6:
                start = 1
                plaintext = rng.randrange(0, 1 << 15)
                key = rng.randrange(0, 1 << 45)
            elif phase == 7:
                start = 0
            elif phase == 8:
                start = 0
                if rng.random() < 0.6:
                    plaintext = rng.randrange(0, 1 << 15)
            elif phase == 9:
                start = 0
            elif phase == 10:
                start = 1
                plaintext = rng.randrange(0, 1 << 15)
                key = rng.randrange(0, 1 << 45)
            elif phase == 11:
                start = 0
            elif phase == 12:
                start = 0
                if rng.random() < 0.5:
                    key = rng.randrange(0, 1 << 45)
            else:
                start = 0
        row = {
            'reset': reset,
            'start': start,
            'plaintext': plaintext & 0x7FFF,
            'key': key & ((1 << 45) - 1),
        }
        if i % 9 == 5:
            row['mid'] = {'start': 0}
        elif i % 11 == 7:
            row['mid'] = {'start': 1}
        elif i % 13 == 3:
            row['mid'] = {'plaintext': rng.randrange(0, 1 << 15)}
        rows.append(row)
    return rows
