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
            phase = (i - reset_len) % 800
            if phase < 200:
                fs = 0
            elif phase < 400:
                fs = 1
            elif phase < 600:
                fs = 2
            else:
                fs = 3
            sub = phase % 100
            if sub < 25:
                in_1 = rng.randrange(0, 1 << 16)
                in_2 = rng.randrange(0, 1 << 16)
                in_3 = rng.randrange(0, 1 << 16)
            elif sub < 50:
                in_1 = rng.randrange(0, 256)
                in_2 = rng.randrange(0, 256)
                in_3 = rng.randrange(0, 256)
            elif sub < 75:
                in_1 = (1 << 16) - 1 - rng.randrange(0, 256)
                in_2 = (1 << 16) - 1 - rng.randrange(0, 256)
                in_3 = (1 << 16) - 1 - rng.randrange(0, 256)
            else:
                v = rng.randrange(0, 1 << 16)
                in_1 = v
                in_2 = (v + 3) & 0xFFFF
                in_3 = (v - 3) & 0xFFFF
        row = {
            'reset': reset,
            'in_1': in_1,
            'in_2': in_2,
            'in_3': in_3,
            'filter_select': fs,
        }
        if i >= reset_len and (i - reset_len) % 17 == 0:
            row['mid'] = {
                'in_1': rng.randrange(0, 1 << 16),
                'in_2': rng.randrange(0, 1 << 16),
                'in_3': rng.randrange(0, 1 << 16),
            }
        rows.append(row)
    return rows
