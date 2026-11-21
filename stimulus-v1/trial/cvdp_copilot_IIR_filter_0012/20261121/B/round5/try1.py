def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        reset = 1 if i < 8 else 0
        if i < 8:
            in_1 = 0
            in_2 = 0
            in_3 = 0
            fs = 0
        else:
            phase = (i - 8) // 80
            sub = (i - 8) % 80
            if phase % 12 == 0:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
                fs = rng.randint(0, 3)
            elif phase % 12 == 1:
                in_1 = 0x0000
                in_2 = 0x0000
                in_3 = 0x0000
                fs = 0
            elif phase % 12 == 2:
                in_1 = 0x7FFF
                in_2 = 0x8000
                in_3 = 0xFFFF
                fs = 1
            elif phase % 12 == 3:
                in_1 = 0x0001
                in_2 = 0x0002
                in_3 = 0x0003
                fs = 2
            elif phase % 12 == 4:
                in_1 = 0xFFFF
                in_2 = 0xFFFE
                in_3 = 0xFFFD
                fs = 3
            elif phase % 12 == 5:
                in_1 = rng.randint(0x8000, 0xFFFF)
                in_2 = rng.randint(0x0000, 0x7FFF)
                in_3 = rng.randint(0x4000, 0xBFFF)
                fs = 0
            elif phase % 12 == 6:
                in_1 = rng.randint(0x0000, 0x00FF)
                in_2 = rng.randint(0xFF00, 0xFFFF)
                in_3 = rng.randint(0x7F00, 0x80FF)
                fs = 1
            elif phase % 12 == 7:
                in_1 = 0x8000
                in_2 = 0x8000
                in_3 = 0x8000
                fs = 2
            elif phase % 12 == 8:
                in_1 = 0x7FFF
                in_2 = 0x7FFF
                in_3 = 0x7FFF
                fs = 3
            elif phase % 12 == 9:
                if sub < 40:
                    in_1 = 0x0000
                    in_2 = 0xFFFF
                    in_3 = 0x8000
                    fs = 0
                else:
                    in_1 = 0x7FFF
                    in_2 = 0x8000
                    in_3 = 0x0001
                    fs = 1
            elif phase % 12 == 10:
                in_1 = (sub * 0x0101) & 0xFFFF
                in_2 = (0xFFFF - sub * 0x0101) & 0xFFFF
                in_3 = (sub * 0x0202) & 0xFFFF
                fs = sub % 4
            else:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
                fs = 3 if sub < 20 else (2 if sub < 40 else (1 if sub < 60 else 0))
        row = {
            'reset': reset,
            'in_1': in_1 & 0xFFFF,
            'in_2': in_2 & 0xFFFF,
            'in_3': in_3 & 0xFFFF,
            'filter_select': fs & 0x3,
        }
        if i >= 8 and i % 37 == 0:
            row['mid'] = {
                'in_1': rng.randint(0, 0xFFFF),
                'in_2': rng.randint(0, 0xFFFF),
                'in_3': rng.randint(0, 0xFFFF),
                'filter_select': rng.randint(0, 3),
            }
        rows.append(row)
    return rows
