def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        if i < 4:
            reset = 1
            in_1 = in_2 = in_3 = 0
            fs = 0
        else:
            reset = 0
            if i < 24:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = rng.randint(0, 3)
            elif i < 124:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = (i // 30) % 4
            elif i < 624:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = rng.randint(0, 3)
            elif i < 1624:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = (i // 100) % 4
            elif i < 2624:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = rng.randint(0, 3)
            elif i < 3624:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = (i // 50) % 4
            else:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = rng.randint(0, 3)
        row = {
            'reset': reset,
            'in_1': in_1,
            'in_2': in_2,
            'in_3': in_3,
            'filter_select': fs,
        }
        rows.append(row)
    return rows
