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
            if i % 11 == 0:
                in_1 = rng.randrange(1 << 16)
            if i % 13 == 0:
                in_2 = rng.randrange(1 << 16)
            if i % 17 == 0:
                in_3 = rng.randrange(1 << 16)
            if i % 211 == 0:
                in_1 = 0
                in_2 = 0
                in_3 = 0
            if i % 307 == 0:
                in_1 = (1 << 16) - 1
                in_2 = (1 << 16) - 1
                in_3 = (1 << 16) - 1
        row = {
            'reset': reset,
            'in_1': in_1,
            'in_2': in_2,
            'in_3': in_3,
            'filter_select': filter_select,
        }
        if i >= 4 and i % 7 == 0:
            mid = {
                'in_1': rng.randrange(1 << 16),
                'in_2': rng.randrange(1 << 16),
                'in_3': rng.randrange(1 << 16),
                'filter_select': rng.randrange(4),
            }
            row['mid'] = mid
        rows.append(row)
    return rows
