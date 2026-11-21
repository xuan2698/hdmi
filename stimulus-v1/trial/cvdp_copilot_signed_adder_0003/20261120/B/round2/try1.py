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
            if r < 0.04:
                clear = 1
                start = 0
                enable = 0
            elif r < 0.14:
                clear = 0
                start = 1
                enable = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 256)
                b = rng.randint(0, 256)
            elif r < 0.24:
                clear = 0
                start = 0
                enable = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 256)
                b = rng.randint(0, 256)
            elif r < 0.32:
                clear = 0
                start = 0
                enable = 0
            elif r < 0.42:
                clear = 0
                start = 1
                enable = 0
                mode = rng.randint(0, 1)
                a = rng.randint(0, 256)
                b = rng.randint(0, 256)
            else:
                clear = 0
                start = 0
                enable = 1
                if rng.random() < 0.35:
                    mode = rng.randint(0, 1)
                if rng.random() < 0.55:
                    a = rng.randint(0, 256)
                if rng.random() < 0.55:
                    b = rng.randint(0, 256)
        row = {
            'i_rst_n': rst_n,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        if rng.random() < 0.35:
            mid = {}
            if rng.random() < 0.5:
                mid['i_start'] = rng.randint(0, 1)
            if rng.random() < 0.5:
                mid['i_enable'] = rng.randint(0, 1)
            if rng.random() < 0.3:
                mid['i_mode'] = rng.randint(0, 1)
            if rng.random() < 0.2:
                mid['i_clear'] = rng.randint(0, 1)
            if rng.random() < 0.45:
                mid['i_operand_a'] = rng.randint(0, 256)
            if rng.random() < 0.45:
                mid['i_operand_b'] = rng.randint(0, 256)
            row['mid'] = mid
        rows.append(row)
    return rows
