def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        reset = 1 if i < 3 else 0
        if i < 3:
            in_1 = 0
            in_2 = 0
            in_3 = 0
            fs = 0
        else:
            seg = (i - 3) // 250
            if seg % 6 == 0:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
                fs = 0
            elif seg % 6 == 1:
                in_1 = rng.randint(0x8000, 0xFFFF)
                in_2 = rng.randint(0x8000, 0xFFFF)
                in_3 = rng.randint(0x8000, 0xFFFF)
                fs = 1
            elif seg % 6 == 2:
                in_1 = rng.randint(0, 0x7FFF)
                in_2 = rng.randint(0, 0x7FFF)
                in_3 = rng.randint(0, 0x7FFF)
                fs = 2
            elif seg % 6 == 3:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
                fs = 3
            elif seg % 6 == 4:
                in_1 = 0x7FFF
                in_2 = 0x8000
                in_3 = 0xFFFF
                fs = rng.randint(0, 2)
            else:
                in_1 = rng.randint(0, 0x00FF)
                in_2 = rng.randint(0xFF00, 0xFFFF)
                in_3 = rng.randint(0x4000, 0xBFFF)
                fs = rng.randint(0, 3)
        row = {
            'reset': reset,
            'in_1': in_1 & 0xFFFF,
            'in_2': in_2 & 0xFFFF,
            'in_3': in_3 & 0xFFFF,
            'filter_select': fs & 0x3,
        }
        if i >= 3 and i % 41 == 0:
            row['mid'] = {
                'in_1': rng.randint(0, 0xFFFF),
                'in_2': rng.randint(0, 0xFFFF),
                'in_3': rng.randint(0, 0xFFFF),
                'filter_select': rng.randint(0, 3),
            }
        rows.append(row)
    return rows
