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
            plaintext = rng.getrandbits(15)
            key = rng.getrandbits(45)
        else:
            reset = 0
            if (i - 4) % 5 == 0:
                start = 1
                plaintext = rng.getrandbits(15)
                key = rng.getrandbits(45)
            else:
                start = 0
        row = {
            'reset': reset,
            'start': start,
            'plaintext': plaintext & 0x7FFF,
            'key': key & 0x1FFFFFFFFFFFF,
        }
        rows.append(row)
    return rows
