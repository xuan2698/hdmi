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
            elif i < 240:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = (i // 60) % 4
            elif i < 1200:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = rng.randint(0, 3)
            elif i < 2400:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = 0
            elif i < 3000:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = 1
            elif i < 3400:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = 2
            elif i < 3700:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = 3
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
        if i % 9 == 5 and i >= 4:
            row['mid'] = {
                'in_1': rng.randint(0, 65535),
                'in_2': rng.randint(0, 65535),
                'in_3': rng.randint(0, 65535),
                'filter_select': rng.randint(0, 3),
            }
        rows.append(row)
    return rows
