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
        elif i < 6:
            reset = 0
            start = 0
            plaintext = rng.randrange(0, 1 << 15)
            key = rng.randrange(0, 1 << 45)
        else:
            reset = 0
            phase = (i - 6) % 12
            if phase == 0:
                start = 1
                plaintext = rng.randrange(0, 1 << 15)
                key = rng.randrange(0, 1 << 45)
            elif phase == 1:
                start = 0
            elif phase == 2:
                start = 0
            elif phase == 3:
                start = 0
            elif phase == 4:
                start = 0
                if rng.random() < 0.5:
                    plaintext = rng.randrange(0, 1 << 15)
            elif phase == 5:
                start = 0
                if rng.random() < 0.5:
                    key = rng.randrange(0, 1 << 45)
            elif phase == 6:
                start = 0
            elif phase == 7:
                start = 0
                if rng.random() < 0.4:
                    plaintext = rng.randrange(0, 1 << 15)
                    key = rng.randrange(0, 1 << 45)
            elif phase == 8:
                start = 0
            elif phase == 9:
                start = 0
                if rng.random() < 0.3:
                    plaintext = rng.randrange(0, 1 << 15)
            elif phase == 10:
                start = 0
            else:
                start = 0
                if rng.random() < 0.25:
                    key = rng.randrange(0, 1 << 45)
        row = {
            'reset': reset,
            'start': start,
            'plaintext': plaintext & 0x7FFF,
            'key': key & ((1 << 45) - 1),
        }
        if i % 7 == 4 and i >= 6:
            row['mid'] = {'start': 0}
        rows.append(row)
    return rows
