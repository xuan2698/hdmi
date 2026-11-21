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
        elif i == 3:
            reset = 0
            start = 0
            plaintext = rng.randrange(0, 1 << 15)
            key = rng.randrange(0, 1 << 45)
        else:
            reset = 0
            if i % 7 == 0:
                start = 1
            else:
                start = 0
            if i % 5 == 0:
                plaintext = rng.randrange(0, 1 << 15)
            if i % 11 == 0:
                key = rng.randrange(0, 1 << 45)
            if i % 29 == 0:
                plaintext = 0
            if i % 31 == 0:
                key = (1 << 45) - 1
            if i % 37 == 0:
                plaintext = (1 << 15) - 1
            if i % 41 == 0:
                key = 0
            if i % 43 == 0:
                plaintext = (rng.randrange(0, 1 << 15)) & 0x7FFF
        row = {
            'reset': reset,
            'start': start,
            'plaintext': plaintext,
            'key': key,
        }
        if i % 13 == 0 and i > 3:
            row['mid'] = {
                'start': 0,
            }
        rows.append(row)
    return rows
