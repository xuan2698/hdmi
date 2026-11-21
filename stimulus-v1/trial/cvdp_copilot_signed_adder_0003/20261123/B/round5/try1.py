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
        else:
            rst_n = 1
            r = rng.random()
            if r < 0.02:
                clear = 1
                start = 0
                enable = 0
                mode = 0
                a = 0
                b = 0
            elif r < 0.06:
                clear = 0
                start = 1
                enable = 1
                mode = 0
                a = 0x7F
                b = 0x01
            elif r < 0.10:
                clear = 0
                start = 1
                enable = 1
                mode = 0
                a = 0x80
                b = 0x80
            elif r < 0.14:
                clear = 0
                start = 1
                enable = 1
                mode = 1
                a = 0x80
                b = 0x01
            elif r < 0.18:
                clear = 0
                start = 1
                enable = 1
                mode = 1
                a = 0x7F
                b = 0xFF
            elif r < 0.22:
                clear = 0
                start = 1
                enable = 1
                mode = 0
                a = 0xFF
                b = 0x01
            elif r < 0.26:
                clear = 0
                start = 1
                enable = 1
                mode = 1
                a = 0x00
                b = 0x80
            elif r < 0.30:
                clear = 0
                start = 1
                enable = 1
                mode = 1
                a = 0x80
                b = 0x80
            elif r < 0.34:
                clear = 0
                start = 1
                enable = 1
                mode = 0
                a = 0x7F
                b = 0x7F
            elif r < 0.42:
                clear = 0
                start = 1
                enable = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.50:
                clear = 0
                start = 0
                enable = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.58:
                clear = 0
                start = 1
                enable = 0
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.66:
                clear = 0
                start = 0
                enable = 0
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.74:
                clear = 0
                start = 1
                enable = 1
                mode = 0
                a = rng.randint(0, 127)
                b = rng.randint(0, 127)
            elif r < 0.82:
                clear = 0
                start = 1
                enable = 1
                mode = 1
                a = rng.randint(128, 255)
                b = rng.randint(128, 255)
            elif r < 0.90:
                clear = 0
                start = 1
                enable = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            else:
                clear = 0
                start = 1
                enable = 1
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
