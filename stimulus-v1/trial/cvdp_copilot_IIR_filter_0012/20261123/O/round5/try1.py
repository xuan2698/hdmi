def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        reset = 1 if i < 4 else 0
        if reset:
            in_1 = in_2 = in_3 = 0
            fs = 0
        else:
            phase = (i - 4) % 400
            if phase < 30:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
            elif phase < 70:
                in_1 = rng.randint(0, 0x00FF)
                in_2 = rng.randint(0, 0x00FF)
                in_3 = rng.randint(0, 0x00FF)
            elif phase < 110:
                in_1 = rng.randint(0xFF00, 0xFFFF)
                in_2 = rng.randint(0xFF00, 0xFFFF)
                in_3 = rng.randint(0xFF00, 0xFFFF)
            elif phase < 150:
                v = rng.randint(0, 0xFFFF)
                in_1 = v
                in_2 = v
                in_3 = v
            elif phase < 190:
                in_1 = 0x7FFF
                in_2 = 0x8000
                in_3 = 0xFFFF
            elif phase < 230:
                in_1 = rng.randint(0x7F00, 0x7FFF)
                in_2 = rng.randint(0x8000, 0x80FF)
                in_3 = rng.randint(0, 0xFFFF)
            elif phase < 270:
                in_1 = 0x0001
                in_2 = 0xFFFF
                in_3 = 0x0000
            elif phase < 310:
                in_1 = rng.randint(0x0000, 0x000F)
                in_2 = rng.randint(0xFFF0, 0xFFFF)
                in_3 = rng.randint(0x7FF0, 0x800F)
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
