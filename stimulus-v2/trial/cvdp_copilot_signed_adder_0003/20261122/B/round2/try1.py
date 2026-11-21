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
        else:
            rst_n = 1
            if i % 89 == 0:
                clear = 1
            else:
                clear = 0
            enable = 1 if rng.random() < 0.82 else 0
            start = 1 if rng.random() < 0.4 else 0
            mode = 1 if rng.random() < 0.5 else 0
            a = rng.randrange(256)
            b = rng.randrange(256)
            if i % 47 == 0:
                enable = 0
                start = 0
            if i % 131 == 0:
                enable = 1
                start = 1
                mode = 0
                a = 0x7F
                b = 0x01
            if i % 173 == 0:
                enable = 1
                start = 1
                mode = 1
                a = 0x80
                b = 0x01
        row = {
            'i_rst_n': rst_n,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        if i >= 4 and rng.random() < 0.28:
            mid = {}
            if rng.random() < 0.5:
                mid['i_operand_a'] = rng.randrange(256)
            if rng.random() < 0.5:
                mid['i_operand_b'] = rng.randrange(256)
            if rng.random() < 0.18:
                mid['i_enable'] = 1 if rng.random() < 0.5 else 0
            if rng.random() < 0.1:
                mid['i_mode'] = 1 if rng.random() < 0.5 else 0
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows
