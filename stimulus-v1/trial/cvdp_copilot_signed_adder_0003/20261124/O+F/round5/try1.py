def stimulus(rng, cycles):
    rows = []
    rst_n = 0
    start = 0
    enable = 0
    mode = 0
    clear = 0
    a = 0
    b = 0
    for i in range(cycles):
        if i < 4:
            rst_n = 0
            start = 0
            enable = 0
            mode = 0
            clear = 0
            a = 0
            b = 0
        elif i == 4:
            rst_n = 1
            start = 0
            enable = 0
            mode = 0
            clear = 0
            a = 0
            b = 0
        else:
            rst_n = 1
            r = rng.random()
            if r < 0.02:
                clear = 1
                start = 0
                enable = 0
                mode = 0
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.10:
                clear = 0
                enable = 1
                start = 1
                mode = rng.randint(0, 1)
                a = rng.choice([0x7F, 0x80, 0xFF, 0x00, 0x01, 0xFE, 0x81, 0x40, 0xC0])
                b = rng.choice([0x7F, 0x80, 0xFF, 0x00, 0x01, 0xFE, 0x81, 0x40, 0xC0])
            elif r < 0.22:
                clear = 0
                enable = 1
                start = 1
                mode = 0
                a = rng.choice([0x7F, 0x80, 0xFF, 0x00, 0x01, 0xFE, 0x81, 0x40, 0xC0])
                b = rng.choice([0x7F, 0x80, 0xFF, 0x00, 0x01, 0xFE, 0x81, 0x40, 0xC0])
            elif r < 0.34:
                clear = 0
                enable = 1
                start = 1
                mode = 1
                a = rng.choice([0x7F, 0x80, 0xFF, 0x00, 0x01, 0xFE, 0x81, 0x40, 0xC0])
                b = rng.choice([0x7F, 0x80, 0xFF, 0x00, 0x01, 0xFE, 0x81, 0x40, 0xC0])
            elif r < 0.50:
                clear = 0
                enable = 1
                start = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.62:
                clear = 0
                enable = 1
                start = 0
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.74:
                clear = 0
                enable = 0
                start = rng.randint(0, 1)
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.86:
                clear = 0
                enable = 1
                start = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            else:
                clear = 0
                enable = rng.randint(0, 1)
                start = rng.randint(0, 1)
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
        row = {
            'i_rst_n': rst_n,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        if rng.random() < 0.25:
            mid = {
                'i_start': rng.randint(0, 1),
                'i_enable': rng.randint(0, 1),
                'i_mode': rng.randint(0, 1),
                'i_clear': 0 if rng.random() < 0.95 else 1,
                'i_operand_a': rng.randint(0, 255),
                'i_operand_b': rng.randint(0, 255),
            }
            row['mid'] = mid
        rows.append(row)
    return rows
