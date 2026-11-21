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
            if r < 0.03:
                clear = 1
                start = 0
                enable = 0
                mode = 0
                a = 0
                b = 0
            elif r < 0.09:
                clear = 0
                enable = 1
                start = 1
                mode = 0
                a = 0x7F
                b = 0x01
            elif r < 0.15:
                clear = 0
                enable = 1
                start = 1
                mode = 0
                a = 0x80
                b = 0x80
            elif r < 0.21:
                clear = 0
                enable = 1
                start = 1
                mode = 1
                a = 0x80
                b = 0x01
            elif r < 0.27:
                clear = 0
                enable = 1
                start = 1
                mode = 1
                a = 0x7F
                b = 0xFF
            elif r < 0.33:
                clear = 0
                enable = 1
                start = 1
                mode = 0
                a = 0xFF
                b = 0xFF
            elif r < 0.39:
                clear = 0
                enable = 1
                start = 1
                mode = 1
                a = 0x00
                b = 0x80
            elif r < 0.44:
                clear = 0
                enable = 1
                start = 1
                mode = 1
                a = 0x80
                b = 0x00
            elif r < 0.49:
                clear = 0
                enable = 1
                start = 1
                mode = 0
                a = 0x7F
                b = 0x7F
            elif r < 0.62:
                clear = 0
                enable = 1
                start = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.72:
                clear = 0
                enable = 1
                start = 0
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.80:
                clear = 0
                enable = 0
                start = rng.randint(0, 1)
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.90:
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
            mid = {}
            if rng.random() < 0.5:
                mid['i_enable'] = rng.randint(0, 1)
            if rng.random() < 0.4:
                mid['i_start'] = rng.randint(0, 1)
            if rng.random() < 0.2:
                mid['i_clear'] = rng.randint(0, 1)
            if rng.random() < 0.3:
                mid['i_operand_a'] = rng.randint(0, 255)
            if rng.random() < 0.3:
                mid['i_operand_b'] = rng.randint(0, 255)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows
