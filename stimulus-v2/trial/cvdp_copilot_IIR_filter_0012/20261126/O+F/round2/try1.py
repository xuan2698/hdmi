def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        if i < 3:
            reset = 1
            in_1 = in_2 = in_3 = 0
            fs = 0
        else:
            reset = 0
            if i < 20:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = rng.randint(0, 3)
            elif i < 200:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = (i // 50) % 4
            elif i < 2000:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = rng.randint(0, 3)
            elif i < 4000:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = 0
            elif i < 6000:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = 1
            elif i < 8000:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = 2
            elif i < 10000:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = 3
            elif i < 12000:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = rng.randint(0, 3)
            elif i < 14000:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = (i // 100) % 4
            elif i < 16000:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = rng.randint(0, 3)
            elif i < 18000:
                in_1 = rng.randint(0, 65535)
                in_2 = rng.randint(0, 65535)
                in_3 = rng.randint(0, 65535)
                fs = rng.randint(0, 3)
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
        if i % 7 == 3 and i >= 3:
            row['mid'] = {
                'in_1': rng.randint(0, 65535),
                'in_2': rng.randint(0, 65535),
                'in_3': rng.randint(0, 65535),
                'filter_select': rng.randint(0, 3),
            }
        rows.append(row)
    return rows
