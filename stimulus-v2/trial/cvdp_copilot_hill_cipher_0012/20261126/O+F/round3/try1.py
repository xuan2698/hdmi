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
            plaintext = rng.randrange(1 << 15)
            key = rng.randrange(1 << 45)
        else:
            reset = 0
            if i % 6 == 4:
                start = 1
            else:
                start = 0
            if i % 6 == 0:
                plaintext = rng.randrange(1 << 15)
                key = rng.randrange(1 << 45)
        row = {
            'reset': reset,
            'start': start,
            'plaintext': plaintext,
            'key': key,
        }
        rows.append(row)
    return rows
