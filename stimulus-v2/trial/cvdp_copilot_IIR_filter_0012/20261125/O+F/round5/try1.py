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
            if i % 7 == 0:
                in_1 = rng.randrange(1 << 16)
            if i % 11 == 0:
                in_2 = rng.randrange(1 << 16)
            if i % 13 == 0:
                in_3 = rng.randrange(1 << 16)
            if i % 197 == 0:
                in_1 = 0
                in_2 = 0
                in_3 = 0
            if i % 293 == 0:
                in_1 = 0xFFFF
                in_2 = 0xFFFF
                in_3 = 0xFFFF
            if i % 389 == 0:
                in_1 = 0x8000
                in_2 = 0x7FFF
                in_3 = 0x0001
            if i % 503 == 0:
                in_1 = 0x7FFF
                in_2 = 0x8000
                in_3 = 0xFFFE
            if i % 601 == 0:
                filter_select = 0
            if i % 701 == 0:
                filter_select = 1
            if i % 809 == 0:
                filter_select = 2
            if i % 907 == 0:
                filter_select = 3
        row = {
            'reset': reset,
            'in_1': in_1 & 0xFFFF,
            'in_2': in_2 & 0xFFFF,
            'in_3': in_3 & 0xFFFF,
            'filter_select': filter_select & 0x3,
        }
        if i >= 4 and i % 5 == 0:
            mid = {
                'in_1': rng.randrange(1 << 16),
                'in_2': rng.randrange(1 << 16),
                'in_3': rng.randrange(1 << 16),
                'filter_select': rng.randrange(4),
            }
            row['mid'] = mid
        rows.append(row)
    return rows
