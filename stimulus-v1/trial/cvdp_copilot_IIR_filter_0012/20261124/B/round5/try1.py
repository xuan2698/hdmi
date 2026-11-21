def stimulus(rng, cycles):
    rows = []
    reset_len = 8
    for i in range(cycles):
        reset = 1 if i < reset_len else 0
        if i < reset_len:
            in_1 = 0
            in_2 = 0
            in_3 = 0
            fs = 0
        else:
            phase = (i - reset_len) % 1000
            if phase < 250:
                fs = 0
            elif phase < 500:
                fs = 1
            elif phase < 750:
                fs = 2
            else:
                fs = 3
            sub = phase % 125
            if sub < 30:
                in_1 = rng.randrange(0, 1 << 16)
                in_2 = rng.randrange(0, 1 << 16)
                in_3 = rng.randrange(0, 1 << 16)
            elif sub < 60:
                in_1 = rng.randrange(0, 512)
                in_2 = rng.randrange(0, 512)
                in_3 = rng.randrange(0, 512)
            elif sub < 90:
                in_1 = (1 << 16) - 1 - rng.randrange(0, 512)
                in_2 = (1 << 16) - 1 - rng.randrange(0, 512)
                in_3 = (1 << 16) - 1 - rng.randrange(0, 512)
            elif sub < 110:
                v = rng.randrange(0, 1 << 16)
                in_1 = v
                in_2 = (v + 7) & 0xFFFF
                in_3 = (v - 7) & 0xFFFF
            else:
                in_1 = 0x8000
                in_2 = 0x7FFF
                in_3 = 0xFFFF
        row = {
            'reset': reset,
            'in_1': in_1,
            'in_2': in_2,
            'in_3': in_3,
            'filter_select': fs,
        }
        if i >= reset_len and (i - reset_len) % 23 == 0:
            row['mid'] = {
                'in_1': rng.randrange(0, 1 << 16),
                'in_2': rng.randrange(0, 1 << 16),
                'in_3': rng.randrange(0, 1 << 16),
            }
        rows.append(row)
    return rows
