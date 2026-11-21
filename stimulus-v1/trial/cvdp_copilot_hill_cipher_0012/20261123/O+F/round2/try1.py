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
        elif i < 8:
            reset = 0
            start = 0
            plaintext = rng.randrange(0, 1 << 15)
            key = rng.randrange(0, 1 << 45)
        else:
            reset = 0
            phase = (i - 8) % 9
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
                if rng.random() < 0.4:
                    key = rng.randrange(0, 1 << 45)
            elif phase == 6:
                start = 0
            elif phase == 7:
                start = 0
                if rng.random() < 0.3:
                    plaintext = rng.randrange(0, 1 << 15)
                    key = rng.randrange(0, 1 << 45)
            else:
                start = 0
        row = {
            'reset': reset,
            'start': start,
            'plaintext': plaintext & 0x7FFF,
            'key': key & ((1 << 45) - 1),
        }
        mid = {}
        if i >= 8 and (i - 8) % 9 == 0:
            mid['start'] = 0
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows
