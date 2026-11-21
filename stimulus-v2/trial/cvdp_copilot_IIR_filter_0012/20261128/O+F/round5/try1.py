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
            if i % 89 == 0:
                in_1 = rng.randrange(0, 65536)
                in_2 = rng.randrange(0, 65536)
                in_3 = rng.randrange(0, 65536)
            if i % 53 == 0:
                filter_select = rng.randrange(0, 4)
            if i % 31 == 0:
                in_1 = (in_1 + rng.randrange(0, 8192)) % 65536
            if i % 41 == 0:
                in_2 = (in_2 + rng.randrange(0, 8192)) % 65536
            if i % 59 == 0:
                in_3 = (in_3 + rng.randrange(0, 8192)) % 65536
            if i % 127 == 0:
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
            if i % 397 == 0:
                in_1 = 1
                in_2 = 2
                in_3 = 3
            if i % 499 == 0:
                in_1 = 65534
                in_2 = 65533
                in_3 = 65532
            if i % 587 == 0:
                filter_select = 0
            if i % 593 == 0:
                filter_select = 1
            if i % 599 == 0:
                filter_select = 2
            if i % 601 == 0:
                filter_select = 3
            if i % 701 == 0:
                reset = 1
            if i % 701 == 2:
                reset = 0
        row = {
            'reset': reset,
            'in_1': in_1,
            'in_2': in_2,
            'in_3': in_3,
            'filter_select': filter_select,
        }
        if i >= 3 and i % 13 == 0:
            row['mid'] = {
                'in_1': rng.randrange(0, 65536),
                'in_2': rng.randrange(0, 65536),
                'in_3': rng.randrange(0, 65536),
                'filter_select': rng.randrange(0, 4),
            }
        rows.append(row)
    return rows
