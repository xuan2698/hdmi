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
            plaintext = rng.randrange(1 << 15)
            key = rng.randrange(1 << 45)
        else:
            reset = 0
            phase = (i - 2) % 5
            if phase == 0:
                start = 1
                plaintext = rng.randrange(1 << 15)
                key = rng.randrange(1 << 45)
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
