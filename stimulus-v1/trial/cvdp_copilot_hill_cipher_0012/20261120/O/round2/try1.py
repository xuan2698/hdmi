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
            if i % 4 == 0:
                plaintext = rng.randrange(0, 1 << 15)
            if i % 9 == 0:
                key = rng.randrange(0, 1 << 45)
        row = {
            'reset': reset,
            'start': start,
            'plaintext': plaintext,
            'key': key,
        }
        if i % 10 == 0 and i > 4:
            row['mid'] = {
                'start': 0,
            }
        rows.append(row)
    return rows
