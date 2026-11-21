def stimulus(rng, cycles):
    rows = []
    reset = 1
    in_1 = 0
    in_2 = 0
    in_3 = 0
    filter_select = 0
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i == 3:
            reset = 0
        if i >= 3:
            if i % 4 == 0:
                in_1 = rng.randrange(0, 1 << 16)
            if i % 6 == 0:
                in_2 = rng.randrange(0, 1 << 16)
            if i % 8 == 0:
                in_3 = rng.randrange(0, 1 << 16)
            if i % 9 == 0:
                filter_select = rng.randrange(0, 4)
            if i % 12 == 0:
                in_1 = 0
                in_2 = 0
                in_3 = 0
            if i % 15 == 0:
                in_1 = 0xFFFF
                in_2 = 0xFFFF
                in_3 = 0xFFFF
            if i % 18 == 0:
                in_1 = 0x8000
                in_2 = 0x8000
                in_3 = 0x8000
            if i % 21 == 0:
                in_1 = 0x7FFF
                in_2 = 0x7FFF
                in_3 = 0x7FFF
            if i % 24 == 0:
                filter_select = 0
            if i % 27 == 0:
                filter_select = 1
            if i % 30 == 0:
                filter_select = 2
            if i % 33 == 0:
                filter_select = 3
            if i % 36 == 0:
                in_1 = (in_1 + 1) & 0xFFFF
                in_2 = (in_2 + 1) & 0xFFFF
                in_3 = (in_3 + 1) & 0xFFFF
            if i % 40 == 0:
                in_1 = 0x0001
                in_2 = 0x0002
                in_3 = 0x0003
            if i % 44 == 0:
                in_1 = 0xFFFE
                in_2 = 0xFFFD
                in_3 = 0xFFFC
            if i % 50 == 0:
                in_1 = rng.randrange(0, 1 << 16)
                in_2 = rng.randrange(0, 1 << 16)
                in_3 = rng.randrange(0, 1 << 16)
                filter_select = rng.randrange(0, 4)
        row = {
            'reset': reset,
            'in_1': in_1,
            'in_2': in_2,
            'in_3': in_3,
            'filter_select': filter_select,
        }
        if i % 5 == 0 and i >= 3:
            row['mid'] = {
                'in_1': rng.randrange(0, 1 << 16),
                'in_2': rng.randrange(0, 1 << 16),
                'in_3': rng.randrange(0, 1 << 16),
                'filter_select': rng.randrange(0, 4),
            }
        rows.append(row)
    return rows
