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
            phase = (i - 3) // 120
            p = phase % 10
            if p == 0:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
                fs = 0
            elif p == 1:
                in_1 = rng.randint(0x7F00, 0x80FF)
                in_2 = rng.randint(0x7F00, 0x80FF)
                in_3 = rng.randint(0x7F00, 0x80FF)
                fs = 1
            elif p == 2:
                in_1 = rng.randint(0x8000, 0xFFFF)
                in_2 = rng.randint(0, 0x7FFF)
                in_3 = rng.randint(0x4000, 0xBFFF)
                fs = 2
            elif p == 3:
                in_1 = rng.randint(0, 0x00FF)
                in_2 = rng.randint(0xFF00, 0xFFFF)
                in_3 = rng.randint(0x7F00, 0x80FF)
                fs = 3
            elif p == 4:
                in_1 = 0x7FFF
                in_2 = 0x8000
                in_3 = 0xFFFF
                fs = 0
            elif p == 5:
                in_1 = 0
                in_2 = 0
                in_3 = 0
                fs = 1
            elif p == 6:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
                fs = 2
            elif p == 7:
                in_1 = rng.randint(0x7F00, 0x80FF)
                in_2 = rng.randint(0x7F00, 0x80FF)
                in_3 = rng.randint(0x7F00, 0x80FF)
                fs = 3
            elif p == 8:
                in_1 = 0x0001
                in_2 = 0xFFFF
                in_3 = 0x0000
                fs = 0
            else:
                in_1 = rng.randint(0x4000, 0xC000)
                in_2 = rng.randint(0x4000, 0xC000)
                in_3 = rng.randint(0x4000, 0xC000)
                fs = 1
        row = {
            'reset': reset,
            'in_1': in_1 & 0xFFFF,
            'in_2': in_2 & 0xFFFF,
            'in_3': in_3 & 0xFFFF,
            'filter_select': fs & 0x3,
        }
        if i >= 3 and i % 47 == 0:
            row['mid'] = {
                'in_1': rng.randint(0, 0xFFFF),
                'in_2': rng.randint(0, 0xFFFF),
                'in_3': rng.randint(0, 0xFFFF),
                'filter_select': rng.randint(0, 3),
            }
        rows.append(row)
    return rows
