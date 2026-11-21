def stimulus(rng, cycles):
    rows = []
    reset = 1
    in_1 = 0
    in_2 = 0
    in_3 = 0
    fs = 0
    for i in range(cycles):
        if i < 4:
            reset = 1
        elif i == 4:
            reset = 0
        if i >= 4:
            r = rng.random()
            if r < 0.06:
                in_1 = rng.randint(0, 0xFFFF)
            elif r < 0.12:
                in_1 = rng.randint(0, 0x00FF)
            elif r < 0.18:
                in_1 = rng.randint(0xFF00, 0xFFFF)
            elif r < 0.22:
                in_1 = 0
            if rng.random() < 0.09:
                in_2 = rng.randint(0, 0xFFFF)
            if rng.random() < 0.09:
                in_3 = rng.randint(0, 0xFFFF)
            if rng.random() < 0.04:
                fs = rng.randint(0, 3)
            if i % 400 == 0 and i > 0:
                in_1 = rng.randint(0, 0xFFFF)
                in_2 = rng.randint(0, 0xFFFF)
                in_3 = rng.randint(0, 0xFFFF)
            if i % 700 == 0 and i > 0:
                fs = (fs + 1) & 0x3
        row = {
            'reset': reset,
            'in_1': in_1 & 0xFFFF,
            'in_2': in_2 & 0xFFFF,
            'in_3': in_3 & 0xFFFF,
            'filter_select': fs & 0x3,
        }
        rows.append(row)
    return rows
