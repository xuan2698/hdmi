def stimulus(rng, cycles):
    rows = []
    reset = 1
    in_1 = 0
    in_2 = 0
    in_3 = 0
    filter_select = 0
    for i in range(cycles):
        if i < 4:
            reset = 1
        elif i == 4:
            reset = 0
        if i >= 4:
            if i % 89 == 0:
                filter_select = rng.randrange(4)
            if i % 5 == 0:
                in_1 = rng.randrange(1 << 16)
            if i % 9 == 0:
                in_2 = rng.randrange(1 << 16)
            if i % 13 == 0:
                in_3 = rng.randrange(1 << 16)
            if i % 173 == 0:
                in_1 = 0
                in_2 = 0
                in_3 = 0
            if i % 229 == 0:
                in_1 = 0xFFFF
                in_2 = 0xFFFF
                in_3 = 0xFFFF
            if i % 281 == 0:
                in_1 = 0x8000
                in_2 = 0x7FFF
                in_3 = 0x8000
            if i % 337 == 0:
                in_1 = 0x7FFF
                in_2 = 0x8000
                in_3 = 0x7FFF
            if i % 401 == 0:
                filter_select = 0
            if i % 419 == 0:
                filter_select = 1
            if i % 433 == 0:
                filter_select = 2
            if i % 449 == 0:
                filter_select = 3
        row = {
            'reset': reset,
            'in_1': in_1,
            'in_2': in_2,
            'in_3': in_3,
            'filter_select': filter_select,
        }
        if i >= 4 and i % 7 == 0:
            row['mid'] = {
                'in_1': rng.randrange(1 << 16),
                'in_2': rng.randrange(1 << 16),
                'in_3': rng.randrange(1 << 16),
            }
        rows.append(row)
    return rows
