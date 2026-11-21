def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        reset = 1 if i < 4 else 0
        if i < 4:
            in_1 = in_2 = in_3 = 0
            fs = 0
        else:
            phase = (i - 4) % 240
            if phase < 30:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
            elif phase < 60:
                in_1 = rng.randint(0, 0x0007)
                in_2 = rng.randint(0, 0x0007)
                in_3 = rng.randint(0, 0x0007)
            elif phase < 90:
                in_1 = rng.randint(0xFFF8, 0xFFFF)
                in_2 = rng.randint(0xFFF8, 0xFFFF)
                in_3 = rng.randint(0xFFF8, 0xFFFF)
            elif phase < 120:
                v = rng.randint(0, 0xFFFF)
                in_1 = v
                in_2 = v
                in_3 = v
            elif phase < 150:
                in_1 = rng.randint(0x7FF8, 0x8007)
                in_2 = rng.randint(0x7FF8, 0x8007)
                in_3 = rng.randint(0x7FF8, 0x8007)
            elif phase < 180:
                in_1 = rng.randint(0, 0x00FF)
                in_2 = rng.randint(0xFF00, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
            elif phase < 210:
                in_1 = rng.randint(0x8000, 0xFFFF)
                in_2 = rng.randint(0, 0x7FFF)
                in_3 = rng.randint(0, 0xFFFF)
            else:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
            fs = (i // 60) % 4
        row = {
            'reset': reset,
            'in_1': in_1 & 0xFFFF,
            'in_2': in_2 & 0xFFFF,
            'in_3': in_3 & 0xFFFF,
            'filter_select': fs & 0x3,
        }
        if i >= 4 and (i % 11 == 0):
            row['mid'] = {
                'in_1': rng.randint(0, 0xFFFF),
                'in_2': rng.randint(0, 0xFFFF),
                'in_3': rng.randint(0, 0xFFFF),
            }
        rows.append(row)
    return rows
