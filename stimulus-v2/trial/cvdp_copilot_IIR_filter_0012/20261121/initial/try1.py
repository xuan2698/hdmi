def stimulus(rng, cycles):
    rows = []
    reset = 1
    in_1 = 0
    in_2 = 0
    in_3 = 0
    fs = 0
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i == 3:
            reset = 0
        if i >= 3:
            r = rng.random()
            if r < 0.05:
                in_1 = rng.randint(0, 0xFFFF)
            elif r < 0.10:
                in_1 = rng.randint(0, 0x00FF)
            elif r < 0.15:
                in_1 = rng.randint(0xFF00, 0xFFFF)
            if rng.random() < 0.08:
                in_2 = rng.randint(0, 0xFFFF)
            if rng.random() < 0.08:
                in_3 = rng.randint(0, 0xFFFF)
            if rng.random() < 0.03:
                fs = rng.randint(0, 3)
            if i % 500 == 0 and i > 0:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
        row = {
            'reset': reset,
            'in_1': in_1 & 0xFFFF,
            'in_2': in_2 & 0xFFFF,
            'in_3': in_3 & 0xFFFF,
            'filter_select': fs & 0x3,
        }
        rows.append(row)
    return rows
