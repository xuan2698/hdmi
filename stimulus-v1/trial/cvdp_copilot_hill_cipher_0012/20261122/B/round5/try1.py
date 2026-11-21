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
        elif i == 5:
            reset = 0
            start = 0
            plaintext = rng.randrange(0, 1 << 15)
            key = rng.randrange(0, 1 << 45)
        else:
            reset = 0
            if i % 5 == 0:
                start = 1
            else:
                start = 0
            if i % 3 == 0:
                plaintext = rng.randrange(0, 1 << 15)
            if i % 7 == 0:
                key = rng.randrange(0, 1 << 45)
            if i % 11 == 0:
                plaintext = 0
            if i % 13 == 0:
                key = 0
            if i % 17 == 0:
                plaintext = (1 << 15) - 1
            if i % 19 == 0:
                key = (1 << 45) - 1
            if i % 23 == 0:
                plaintext = rng.randrange(0, 1 << 15)
                key = rng.randrange(0, 1 << 45)
            if i % 29 == 0 and i > 15:
                reset = 1
                start = 0
            if i % 37 == 0:
                plaintext = (rng.randrange(0, 32) << 10) | (rng.randrange(0, 32) << 5) | rng.randrange(0, 32)
            if i % 41 == 0:
                key = 0
                for _ in range(9):
                    key = (key << 5) | rng.randrange(0, 32)
        row = {
            'reset': reset,
            'start': start,
            'plaintext': plaintext,
            'key': key,
        }
        if i % 6 == 0 and i > 5:
            row['mid'] = {
                'start': 0,
            }
        rows.append(row)
    return rows
