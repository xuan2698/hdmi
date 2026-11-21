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
            elif r < 0.10:
                clear = 0
                enable = 1
                start = 1
                mode = 0
                a = 0x7F
                b = 0x01
            elif r < 0.17:
                clear = 0
                enable = 1
                start = 1
                mode = 0
                a = 0x80
                b = 0x80
            elif r < 0.24:
                clear = 0
                enable = 1
                start = 1
                mode = 1
                a = 0x80
                b = 0x01
            elif r < 0.31:
                clear = 0
                enable = 1
                start = 1
                mode = 1
                a = 0x7F
                b = 0xFF
            elif r < 0.38:
                clear = 0
                enable = 1
                start = 1
                mode = 0
                a = 0xFF
                b = 0x01
            elif r < 0.45:
                clear = 0
                enable = 1
                start = 1
                mode = 1
                a = 0x00
                b = 0x80
            elif r < 0.52:
                clear = 0
                enable = 1
                start = 1
                mode = 0
                a = 0x7F
                b = 0x7F
            elif r < 0.59:
                clear = 0
                enable = 1
                start = 1
                mode = 1
                a = 0x80
                b = 0x80
            elif r < 0.66:
                clear = 0
                enable = 1
                start = 1
                mode = rng.randint(0, 1)
                a = rng.choice([0x00, 0x01, 0x7F, 0x80, 0xFF])
                b = rng.choice([0x00, 0x01, 0x7F, 0x80, 0xFF])
            elif r < 0.74:
                clear = 0
                enable = 1
                start = 0
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.82:
                clear = 0
                enable = 0
                start = rng.randint(0, 1)
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
        if rng.random() < 0.30:
            mid = {}
            if rng.random() < 0.5:
                mid['i_enable'] = rng.randint(0, 1)
            if rng.random() < 0.5:
                mid['i_start'] = rng.randint(0, 1)
            if rng.random() < 0.25:
                mid['i_clear'] = rng.randint(0, 1)
            if rng.random() < 0.25:
                mid['i_mode'] = rng.randint(0, 1)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows
