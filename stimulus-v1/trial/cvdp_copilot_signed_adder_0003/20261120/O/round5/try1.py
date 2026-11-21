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
        elif i < 10:
            rst_n = 1
            clear = 0
            start = 1
            enable = 1
            mode = 0
            a = 0x7F
            b = 0x01
        elif i < 16:
            rst_n = 1
            clear = 0
            start = 0
            enable = 1
            mode = 0
            a = 0x80
            b = 0x80
        elif i < 22:
            rst_n = 1
            clear = 0
            start = 0
            enable = 1
            mode = 1
            a = 0x80
            b = 0x01
        elif i < 28:
            rst_n = 1
            clear = 0
            start = 0
            enable = 1
            mode = 1
            a = 0x7F
            b = 0xFF
        elif i < 34:
            rst_n = 1
            clear = 0
            start = 0
            enable = 0
            mode = 0
            a = 0
            b = 0
        elif i < 40:
            rst_n = 1
            clear = 1
            start = 0
            enable = 0
            mode = 0
            a = 0
            b = 0
        elif i < 46:
            rst_n = 1
            clear = 0
            start = 1
            enable = 1
            mode = 1
            a = 0x55
            b = 0xAA
        else:
            rst_n = 1
            r = rng.random()
            if r < 0.03:
                clear = 1
                start = 0
                enable = 0
            elif r < 0.13:
                clear = 0
                start = 1
                enable = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.23:
                clear = 0
                start = 0
                enable = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.33:
                clear = 0
                start = 0
                enable = 0
            else:
                clear = 0
                start = 0
                enable = 1
                if rng.random() < 0.3:
                    mode = rng.randint(0, 1)
                if rng.random() < 0.5:
                    a = rng.randint(0, 255)
                if rng.random() < 0.5:
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
        if rng.random() < 0.3:
            mid = {}
            if rng.random() < 0.5:
                mid['i_start'] = rng.randint(0, 1)
            if rng.random() < 0.5:
                mid['i_enable'] = rng.randint(0, 1)
            if rng.random() < 0.3:
                mid['i_mode'] = rng.randint(0, 1)
            if rng.random() < 0.2:
                mid['i_clear'] = rng.randint(0, 1)
            if rng.random() < 0.4:
                mid['i_operand_a'] = rng.randint(0, 255)
            if rng.random() < 0.4:
                mid['i_operand_b'] = rng.randint(0, 255)
            row['mid'] = mid
        rows.append(row)
    return rows
