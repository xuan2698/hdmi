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
            if i % 97 == 0:
                in_1 = rng.randrange(0, 65536)
                in_2 = rng.randrange(0, 65536)
                in_3 = rng.randrange(0, 65536)
            if i % 61 == 0:
                filter_select = rng.randrange(0, 4)
            if i % 37 == 0:
                in_1 = (in_1 + rng.randrange(0, 4096)) % 65536
            if i % 43 == 0:
                in_2 = (in_2 + rng.randrange(0, 4096)) % 65536
            if i % 47 == 0:
                in_3 = (in_3 + rng.randrange(0, 4096)) % 65536
            if i % 149 == 0:
                in_1 = 0
                in_2 = 0
                in_3 = 0
            if i % 223 == 0:
                in_1 = 65535
                in_2 = 65535
                in_3 = 65535
            if i % 311 == 0:
                in_1 = 32768
                in_2 = 32768
                in_3 = 32768
            if i % 401 == 0:
                in_1 = 1
                in_2 = 2
                in_3 = 3
            if i % 503 == 0:
                in_1 = 65534
                in_2 = 65533
                in_3 = 65532
            if i % 601 == 0:
                filter_select = 0
            if i % 607 == 0:
                filter_select = 1
            if i % 613 == 0:
                filter_select = 2
            if i % 619 == 0:
                filter_select = 3
        row = {
            'reset': reset,
            'in_1': in_1,
            'in_2': in_2,
            'in_3': in_3,
            'filter_select': filter_select,
        }
        if i >= 4 and i % 17 == 0:
            row['mid'] = {
                'in_1': rng.randrange(0, 65536),
                'in_2': rng.randrange(0, 65536),
                'in_3': rng.randrange(0, 65536),
                'filter_select': rng.randrange(0, 4),
            }
        rows.append(row)
    return rows
