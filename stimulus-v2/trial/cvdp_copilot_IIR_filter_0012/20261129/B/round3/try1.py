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
        elif i < 5:
            reset = 0
        if i == 5:
            in_1 = rng.randrange(0, 1 << 16)
            in_2 = rng.randrange(0, 1 << 16)
            in_3 = rng.randrange(0, 1 << 16)
            filter_select = rng.randrange(0, 4)
        elif i > 5 and i % 7 == 0:
            in_1 = rng.randrange(0, 1 << 16)
            in_2 = rng.randrange(0, 1 << 16)
            in_3 = rng.randrange(0, 1 << 16)
        if i > 5 and i % 11 == 0:
            filter_select = rng.randrange(0, 4)
        if i > 5 and i % 13 == 0:
            reset = 1
        elif i > 5 and i % 13 == 1:
            reset = 0
        row = {
            'reset': reset,
            'in_1': in_1,
            'in_2': in_2,
            'in_3': in_3,
            'filter_select': filter_select,
        }
        if i % 5 == 2:
            row['mid'] = {
                'in_1': rng.randrange(0, 1 << 16),
                'in_2': rng.randrange(0, 1 << 16),
                'in_3': rng.randrange(0, 1 << 16),
            }
        rows.append(row)
    return rows
