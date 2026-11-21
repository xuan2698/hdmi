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
            if i % 9 == 0:
                in_1 = rng.randrange(0, 1 << 16)
            if i % 12 == 0:
                in_2 = rng.randrange(0, 1 << 16)
            if i % 15 == 0:
                in_3 = rng.randrange(0, 1 << 16)
            if i % 19 == 0:
                filter_select = rng.randrange(0, 4)
            if i % 101 == 0:
                in_1 = 0
                in_2 = 0
                in_3 = 0
            if i % 211 == 0:
                filter_select = 0
        row = {
            'reset': reset,
            'in_1': in_1,
            'in_2': in_2,
            'in_3': in_3,
            'filter_select': filter_select,
        }
        if i % 6 == 0 and i >= 4:
            row['mid'] = {
                'in_1': rng.randrange(0, 1 << 16),
                'in_2': rng.randrange(0, 1 << 16),
                'in_3': rng.randrange(0, 1 << 16),
                'filter_select': rng.randrange(0, 4),
            }
        rows.append(row)
    return rows
