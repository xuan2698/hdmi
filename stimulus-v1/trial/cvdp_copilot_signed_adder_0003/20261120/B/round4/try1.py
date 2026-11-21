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
        elif i < 12:
            rst_n = 1
            clear = 0
            start = 1
            enable = 1
            mode = i & 1
            a = rng.choice([0x7F, 0x80, 0xFF, 0x01, 0x00, 0x55, 0xAA])
            b = rng.choice([0x01, 0x7F, 0x80, 0xFF, 0x00, 0xAA, 0x55])
        else:
            rst_n = 1
            r = rng.random()
            if r < 0.02:
                clear = 1
                start = 0
                enable = 0
            elif r < 0.10:
                clear = 0
                start = 1
                enable = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.18:
                clear = 0
                start = 0
                enable = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.26:
                clear = 0
                start = 0
                enable = 0
            elif r < 0.34:
                clear = 0
                start = 1
                enable = 0
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.42:
                clear = 0
                start = 0
                enable = 1
                mode = 0
                a = rng.choice([0x7F, 0x80, 0xFF, 0x01, 0x00])
                b = rng.choice([0x01, 0x7F, 0x80, 0xFF, 0x00])
            elif r < 0.50:
                clear = 0
                start = 0
                enable = 1
                mode = 1
                a = rng.choice([0x80, 0x7F, 0x00, 0xFF, 0x01])
                b = rng.choice([0x01, 0x80, 0x7F, 0x00, 0xFF])
            else:
                clear = 0
                start = 0
                enable = 1
                if rng.random() < 0.30:
                    mode = rng.randint(0, 1)
                if rng.random() < 0.50:
                    a = rng.randint(0, 255)
                if rng.random() < 0.50:
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
            if rng.random() < 0.45:
                mid['i_start'] = rng.randint(0, 1)
            if rng.random() < 0.45:
                mid['i_enable'] = rng.randint(0, 1)
            if rng.random() < 0.25:
                mid['i_mode'] = rng.randint(0, 1)
            if rng.random() < 0.15:
                mid['i_clear'] = rng.randint(0, 1)
            if rng.random() < 0.40:
                mid['i_operand_a'] = rng.randint(0, 255)
            if rng.random() < 0.40:
                mid['i_operand_b'] = rng.randint(0, 255)
            row['mid'] = mid
        rows.append(row)
    return rows
