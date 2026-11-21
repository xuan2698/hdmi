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
            if i % 83 == 0:
                in_1 = rng.randrange(0, 65536)
                in_2 = rng.randrange(0, 65536)
                in_3 = rng.randrange(0, 65536)
            if i % 173 == 0:
                filter_select = rng.randrange(0, 4)
            if i % 41 == 0:
                in_1 = (in_1 + rng.randrange(0, 2048)) % 65536
            if i % 53 == 0:
                in_2 = (in_2 + rng.randrange(0, 2048)) % 65536
            if i % 67 == 0:
                in_3 = (in_3 + rng.randrange(0, 2048)) % 65536
            if i % 137 == 0:
                in_1 = 0
                in_2 = 0
                in_3 = 0
            if i % 211 == 0:
                in_1 = 65535
                in_2 = 65535
                in_3 = 65535
            if i % 307 == 0:
                in_1 = 32768
                in_2 = 32768
                in_3 = 32768
        row = {
            'reset': reset,
            'in_1': in_1,
            'in_2': in_2,
            'in_3': in_3,
            'filter_select': filter_select,
        }
        if i % 13 == 0 and i >= 3:
            row['mid'] = {
                'in_1': rng.randrange(0, 65536),
                'in_2': rng.randrange(0, 65536),
                'in_3': rng.randrange(0, 65536),
                'filter_select': rng.randrange(0, 4),
            }
        rows.append(row)
    return rows
