def stimulus(rng, cycles):
    rows = []
    reset = 1
    start = 0
    plaintext = 0
    key = 0
    for i in range(cycles):
        if i < 2:
            reset = 1
            start = 0
            plaintext = 0
            key = 0
        elif i == 2:
            reset = 0
            start = 0
        else:
            reset = 0
            phase = (i - 3) % 8
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
            elif phase == 5:
                start = 0
            elif phase == 6:
                start = 0
            else:
                start = 0
                if rng.randrange(0, 4) == 0:
                    plaintext = rng.randrange(0, 1 << 15)
                    key = rng.randrange(0, 1 << 45)
        row = {
            'reset': reset & 1,
            'start': start & 1,
            'plaintext': plaintext & 0x7FFF,
            'key': key & ((1 << 45) - 1),
        }
        rows.append(row)
    return rows
