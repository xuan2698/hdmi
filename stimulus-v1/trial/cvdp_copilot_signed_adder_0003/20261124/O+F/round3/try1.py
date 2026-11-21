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
        if i < 3:
            rst_n = 0
            start = 0
            enable = 0
            mode = 0
            clear = 0
            a = 0
            b = 0
        elif i == 3:
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
            if r < 0.03:
                clear = 1
                start = 0
                enable = 0
                mode = 0
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.18:
                clear = 0
                enable = 1
                start = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.30:
                clear = 0
                enable = 1
                start = 0
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.42:
                clear = 0
                enable = 0
                start = rng.randint(0, 1)
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.56:
                clear = 0
                enable = 1
                start = 1
                mode = 0
                a = rng.choice([0x7F, 0x80, 0xFF, 0x00, 0x01, 0xFE, 0x81, 0x40, 0xC0])
                b = rng.choice([0x7F, 0x80, 0xFF, 0x00, 0x01, 0xFE, 0x81, 0x40, 0xC0])
            elif r < 0.70:
                clear = 0
                enable = 1
                start = 1
                mode = 1
                a = rng.choice([0x7F, 0x80, 0xFF, 0x00, 0x01, 0xFE, 0x81, 0x40, 0xC0])
                b = rng.choice([0x7F, 0x80, 0xFF, 0x00, 0x01, 0xFE, 0x81, 0x40, 0xC0])
            elif r < 0.82:
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
        if rng.random() < 0.22:
            mid = {
                'i_start': rng.randint(0, 1),
                'i_enable': rng.randint(0, 1),
                'i_mode': rng.randint(0, 1),
                'i_clear': 0 if rng.random() < 0.93 else 1,
                'i_operand_a': rng.randint(0, 255),
                'i_operand_b': rng.randint(0, 255),
            }
            row['mid'] = mid
        rows.append(row)
    return rows
