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
            r = rng.random()
            if r < 0.02:
                clear = 1
                start = 0
                enable = 0
            elif r < 0.05:
                clear = 0
                enable = 0
                start = rng.randint(0, 1)
            elif r < 0.15:
                clear = 0
                enable = 1
                start = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.25:
                clear = 0
                enable = 1
                start = 0
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.33:
                clear = 0
                enable = 0
                start = 0
            elif r < 0.41:
                clear = 0
                enable = 1
                start = 1
                mode = rng.randint(0, 1)
                a = rng.choice([0, 127, 128, 255, 1, 254, 64, 192])
                b = rng.choice([0, 127, 128, 255, 1, 254, 64, 192])
            elif r < 0.49:
                clear = 0
                enable = 1
                start = 1
                mode = 0
                a = rng.choice([0x7F, 0x01, 0x40, 0x80])
                b = rng.choice([0x01, 0x7F, 0x40, 0x80])
            elif r < 0.57:
                clear = 0
                enable = 1
                start = 1
                mode = 1
                a = rng.choice([0x80, 0x00, 0x7F, 0xFF])
                b = rng.choice([0x01, 0x80, 0xFF, 0x00])
            elif r < 0.65:
                clear = 0
                enable = 1
                start = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.73:
                clear = 0
                enable = 1
                start = 0
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.81:
                clear = 0
                enable = 0
                start = 1
                mode = rng.randint(0, 1)
            elif r < 0.89:
                clear = 0
                enable = 1
                start = 1
                mode = 0
                a = rng.choice([0x7F, 0x80, 0xFF, 0x00])
                b = rng.choice([0x01, 0x80, 0xFF, 0x00])
            else:
                clear = 0
                enable = 1
                start = 1
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
        mid = {
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        row['mid'] = mid
        rows.append(row)
    return rows
