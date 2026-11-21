def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        reset = 1 if i < 4 else 0
        if i < 4:
            in_1 = 0
            in_2 = 0
            in_3 = 0
            fs = 0
        else:
            phase = (i - 4) // 200
            if phase % 5 == 0:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
                fs = rng.randint(0, 3)
            elif phase % 5 == 1:
                in_1 = rng.randint(0, 0x00FF)
                in_2 = rng.randint(0xFF00, 0xFFFF)
                in_3 = rng.randint(0x7F00, 0x80FF)
                fs = 0
            elif phase % 5 == 2:
                in_1 = rng.randint(0x8000, 0xFFFF)
                in_2 = rng.randint(0, 0x7FFF)
                in_3 = rng.randint(0x4000, 0xBFFF)
                fs = 1
            elif phase % 5 == 3:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
                fs = 2
            else:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
                fs = 3
        row = {
            'reset': reset,
            'in_1': in_1 & 0xFFFF,
            'in_2': in_2 & 0xFFFF,
            'in_3': in_3 & 0xFFFF,
            'filter_select': fs & 0x3,
        }
        if i >= 4 and i % 37 == 0:
            row['mid'] = {
                'in_1': rng.randint(0, 0xFFFF),
                'in_2': rng.randint(0, 0xFFFF),
                'in_3': rng.randint(0, 0xFFFF),
                'filter_select': rng.randint(0, 3),
            }
        rows.append(row)
    return rows
