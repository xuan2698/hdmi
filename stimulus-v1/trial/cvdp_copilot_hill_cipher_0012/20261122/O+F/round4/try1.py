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
        elif i == 4:
            reset = 0
            start = 0
            plaintext = rng.randrange(0, 1 << 15)
            key = rng.randrange(0, 1 << 45)
        else:
            reset = 0
            if i % 6 == 0:
                start = 1
            else:
                start = 0
            if i % 5 == 0:
                plaintext = rng.randrange(0, 1 << 15)
            if i % 9 == 0:
                key = rng.randrange(0, 1 << 45)
            if i % 23 == 0:
                plaintext = 0
            if i % 27 == 0:
                key = (1 << 45) - 1
            if i % 31 == 0:
                plaintext = (1 << 15) - 1
            if i % 37 == 0:
                key = 0
            if i % 41 == 0:
                plaintext = rng.randrange(0, 1 << 15) & 0x7FFF
            if i % 43 == 0:
                key = rng.randrange(0, 1 << 45) & ((1 << 45) - 1)
            if i % 47 == 0:
                plaintext = (rng.randrange(0, 1 << 15)) | 0x7C00
            if i % 53 == 0:
                key = (rng.randrange(0, 1 << 45)) | 0x1F
        row = {
            'reset': reset,
            'start': start,
            'plaintext': plaintext,
            'key': key,
        }
        if i > 4 and i % 11 == 0:
            row['mid'] = {'start': 0}
        rows.append(row)
    return rows
