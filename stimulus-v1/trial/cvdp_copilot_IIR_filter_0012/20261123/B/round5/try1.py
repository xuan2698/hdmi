def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        reset = 1 if i < 6 else 0
        if i < 6:
            in_1 = in_2 = in_3 = 0
            fs = 0
        else:
            phase = (i - 6) % 500
            if phase < 40:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
            elif phase < 80:
                in_1 = rng.randint(0, 0x0007)
                in_2 = rng.randint(0, 0x0007)
                in_3 = rng.randint(0, 0x0007)
            elif phase < 120:
                in_1 = rng.randint(0xFFF8, 0xFFFF)
                in_2 = rng.randint(0xFFF8, 0xFFFF)
                in_3 = rng.randint(0xFFF8, 0xFFFF)
            elif phase < 160:
                v = rng.randint(0, 0xFFFF)
                in_1 = v
                in_2 = v
                in_3 = v
            elif phase < 200:
                in_1 = rng.randint(0x7FF0, 0x800F)
                in_2 = rng.randint(0x7FF0, 0x800F)
                in_3 = rng.randint(0x7FF0, 0x800F)
            elif phase < 240:
                in_1 = rng.randint(0x0000, 0x0003)
                in_2 = rng.randint(0xFFFD, 0xFFFF)
                in_3 = rng.randint(0x0000, 0x0003)
            elif phase < 280:
                in_1 = 0x8000
                in_2 = 0x7FFF
                in_3 = 0xFFFF
            elif phase < 320:
                in_1 = rng.randint(0x0000, 0x00FF)
                in_2 = rng.randint(0xFF00, 0xFFFF)
                in_3 = rng.randint(0x0000, 0x00FF)
            elif phase < 360:
                in_1 = rng.randint(0x7FFF, 0x8001)
                in_2 = rng.randint(0x7FFF, 0x8001)
                in_3 = rng.randint(0x7FFF, 0x8001)
            else:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
            fs = (i // 70) % 4
        row = {
            'reset': reset,
            'in_1': in_1 & 0xFFFF,
            'in_2': in_2 & 0xFFFF,
            'in_3': in_3 & 0xFFFF,
            'filter_select': fs & 0x3,
        }
        if i >= 6 and (i % 13 == 0):
            row['mid'] = {
                'in_1': rng.randint(0, 0xFFFF),
                'in_2': rng.randint(0, 0xFFFF),
                'in_3': rng.randint(0, 0xFFFF),
            }
        rows.append(row)
    return rows
