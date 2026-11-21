def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        reset = 1 if i < 3 else 0
        if i < 3:
            in_1 = in_2 = in_3 = 0
            fs = 0
        else:
            phase = (i - 3) % 200
            if phase < 20:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
            elif phase < 50:
                in_1 = rng.randint(0, 0x000F)
                in_2 = rng.randint(0, 0x000F)
                in_3 = rng.randint(0, 0x000F)
            elif phase < 80:
                in_1 = rng.randint(0xFFF0, 0xFFFF)
                in_2 = rng.randint(0xFFF0, 0xFFFF)
                in_3 = rng.randint(0xFFF0, 0xFFFF)
            elif phase < 110:
                v = rng.randint(0, 0xFFFF)
                in_1 = v
                in_2 = v
                in_3 = v
            elif phase < 140:
                in_1 = rng.randint(0x7FF0, 0x800F)
                in_2 = rng.randint(0x7FF0, 0x800F)
                in_3 = rng.randint(0x7FF0, 0x800F)
            elif phase < 170:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
            else:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
            fs = (i // 50) % 4
        row = {
            'reset': reset,
            'in_1': in_1 & 0xFFFF,
            'in_2': in_2 & 0xFFFF,
            'in_3': in_3 & 0xFFFF,
            'filter_select': fs & 0x3,
        }
        if i >= 3 and (i % 7 == 0):
            row['mid'] = {
                'in_1': rng.randint(0, 0xFFFF),
                'in_2': rng.randint(0, 0xFFFF),
                'in_3': rng.randint(0, 0xFFFF),
            }
        rows.append(row)
    return rows
