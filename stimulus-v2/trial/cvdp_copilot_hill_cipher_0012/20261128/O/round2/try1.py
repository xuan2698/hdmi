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
        else:
            reset = 0
            phase = (i - 3) % 5
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
            else:
                start = 0
        rows.append({
            'reset': reset & 1,
            'start': start & 1,
            'plaintext': plaintext & 0x7FFF,
            'key': key & ((1 << 45) - 1),
        })
    return rows
