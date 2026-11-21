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
            if i % 7 == 0:
                in_1 = rng.randrange(0, 1 << 16)
            if i % 11 == 0:
                in_2 = rng.randrange(0, 1 << 16)
            if i % 13 == 0:
                in_3 = rng.randrange(0, 1 << 16)
            if i % 17 == 0:
                filter_select = rng.randrange(0, 4)
            if i % 19 == 0:
                in_1 = 0
                in_2 = 0
                in_3 = 0
            if i % 23 == 0:
                in_1 = (1 << 16) - 1
                in_2 = (1 << 16) - 1
                in_3 = (1 << 16) - 1
            if i % 29 == 0:
                filter_select = 0
            if i % 31 == 0:
                filter_select = 1
            if i % 37 == 0:
                filter_select = 2
            if i % 41 == 0:
                filter_select = 3
            if i % 43 == 0:
                in_1 = 0x8000
                in_2 = 0x8000
                in_3 = 0x8000
            if i % 47 == 0:
                in_1 = 0x7FFF
                in_2 = 0x7FFF
                in_3 = 0x7FFF
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
