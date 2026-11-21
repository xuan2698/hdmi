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
        else:
            reset = 0
            if i == 2:
                start = 1
                plaintext = rng.randrange(0, 2**15)
                key = rng.randrange(0, 2**45)
            elif i == 3:
                start = 0
            elif i % 6 == 0:
                start = 1
                plaintext = rng.randrange(0, 2**15)
                key = rng.randrange(0, 2**45)
            elif i % 6 == 1:
                start = 0
            elif i % 6 == 2:
                start = 0
            elif i % 6 == 3:
                start = 0
            elif i % 6 == 4:
                start = 0
            else:
                start = 0
        row = {
            'reset': reset,
            'start': start,
            'plaintext': plaintext,
            'key': key,
        }
        rows.append(row)
    return rows
