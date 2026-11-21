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
            phase = (i - 10) % 11
            if phase == 0:
                start = 1
                plaintext = rng.randrange(0, 1 << 15)
                key = rng.randrange(0, 1 << 45)
            elif phase == 1:
                start = 0
            elif phase == 2:
                start = 0
                if rng.random() < 0.3:
                    plaintext = rng.randrange(0, 1 << 15)
            elif phase == 3:
                start = 0
            elif phase == 4:
                start = 0
                if rng.random() < 0.4:
                    key = rng.randrange(0, 1 << 45)
            elif phase == 5:
                start = 0
            elif phase == 6:
                start = 0
                if rng.random() < 0.25:
                    plaintext = rng.randrange(0, 1 << 15)
                    key = rng.randrange(0, 1 << 45)
            elif phase == 7:
                start = 0
            elif phase == 8:
                start = 0
                if rng.random() < 0.2:
                    plaintext = rng.randrange(0, 1 << 15)
            elif phase == 9:
                start = 0
            else:
                start = 0
                if rng.random() < 0.15:
                    key = rng.randrange(0, 1 << 45)
        row = {
            'reset': reset,
            'start': start,
            'plaintext': plaintext & 0x7FFF,
            'key': key & ((1 << 45) - 1),
        }
        mid = {}
        if i >= 10 and (i - 10) % 11 == 0:
            mid['start'] = 0
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows
