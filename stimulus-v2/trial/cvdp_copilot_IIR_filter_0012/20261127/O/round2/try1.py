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
            if i % 97 == 0:
                filter_select = rng.randrange(4)
            if i % 13 == 0:
                in_1 = rng.randrange(1 << 16)
            if i % 17 == 0:
                in_2 = rng.randrange(1 << 16)
            if i % 19 == 0:
                in_3 = rng.randrange(1 << 16)
            if i % 211 == 0:
                in_1 = 0
                in_2 = 0
                in_3 = 0
            if i % 401 == 0:
                in_1 = 0xFFFF
                in_2 = 0x8000
                in_3 = 0x7FFF
            if i % 503 == 0:
                filter_select = 3
            if i % 601 == 0:
                filter_select = 0
        row = {
            'reset': reset,
            'in_1': in_1 & 0xFFFF,
            'in_2': in_2 & 0xFFFF,
            'in_3': in_3 & 0xFFFF,
            'filter_select': filter_select & 0x3,
        }
        rows.append(row)
    return rows
