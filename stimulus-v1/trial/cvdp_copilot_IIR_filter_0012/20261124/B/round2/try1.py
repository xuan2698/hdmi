def stimulus(rng, cycles):
    rows = []
    reset_len = 6
    for i in range(cycles):
        reset = 1 if i < reset_len else 0
        if i < reset_len:
            in_1 = 0
            in_2 = 0
            in_3 = 0
            fs = 0
        else:
            phase = (i - reset_len) % 512
            if phase < 128:
                fs = 0
            elif phase < 256:
                fs = 1
            elif phase < 384:
                fs = 2
            else:
                fs = 3
            sub = phase % 64
            if sub < 16:
                in_1 = rng.randrange(0, 1 << 16)
                in_2 = rng.randrange(0, 1 << 16)
                in_3 = rng.randrange(0, 1 << 16)
            elif sub < 32:
                in_1 = rng.randrange(0, 512)
                in_2 = rng.randrange(0, 512)
                in_3 = rng.randrange(0, 512)
            elif sub < 48:
                in_1 = (1 << 16) - 1 - rng.randrange(0, 512)
                in_2 = (1 << 16) - 1 - rng.randrange(0, 512)
                in_3 = (1 << 16) - 1 - rng.randrange(0, 512)
            else:
                v = rng.randrange(0, 1 << 16)
                in_1 = v
                in_2 = v
                in_3 = v
        row = {
            'reset': reset,
            'in_1': in_1,
            'in_2': in_2,
            'in_3': in_3,
            'filter_select': fs,
        }
        if i >= reset_len and (i - reset_len) % 11 == 0:
            row['mid'] = {
                'in_1': rng.randrange(0, 1 << 16),
                'in_2': rng.randrange(0, 1 << 16),
                'in_3': rng.randrange(0, 1 << 16),
            }
        rows.append(row)
    return rows
