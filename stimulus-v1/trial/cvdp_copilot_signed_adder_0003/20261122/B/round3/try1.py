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
        if i < 2:
            rst_n = 0
            start = 0
            enable = 0
            mode = 0
            clear = 0
            a = 0
            b = 0
        elif i == 2:
            rst_n = 1
            start = 0
            enable = 0
            mode = 0
            clear = 0
            a = 0
            b = 0
        elif i < 8:
            rst_n = 1
            clear = 0
            enable = 1
            start = 1
            mode = 0
            a = 0x7F
            b = 0x01
        elif i < 14:
            rst_n = 1
            clear = 0
            enable = 1
            start = 1
            mode = 1
            a = 0x80
            b = 0x01
        elif i < 20:
            rst_n = 1
            clear = 0
            enable = 1
            start = 1
            mode = 0
            a = 0xFF
            b = 0xFF
        elif i < 26:
            rst_n = 1
            clear = 0
            enable = 1
            start = 1
            mode = 1
            a = 0x7F
            b = 0xFF
        elif i < 30:
            rst_n = 1
            clear = 1
            enable = 0
            start = 0
            mode = 0
            a = 0
            b = 0
        else:
            r = rng.random()
            rst_n = 1
            if r < 0.04:
                clear = 1
                start = 0
                enable = 0
                mode = 0
            elif r < 0.10:
                clear = 0
                enable = 0
                start = rng.randint(0, 1)
                mode = rng.randint(0, 1)
            elif r < 0.18:
                clear = 0
                enable = 1
                start = 0
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.30:
                clear = 0
                enable = 0
                start = 0
                mode = 0
            else:
                clear = 0
                enable = 1
                start = 1
                mode = rng.randint(0, 1)
                if rng.random() < 0.35:
                    a = rng.choice([0, 1, 0x7F, 0x80, 0xFE, 0xFF])
                    b = rng.choice([0, 1, 0x7F, 0x80, 0xFE, 0xFF])
                else:
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
