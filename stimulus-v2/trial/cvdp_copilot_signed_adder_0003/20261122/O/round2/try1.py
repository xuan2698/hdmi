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
        else:
            rst_n = 1
            if i % 97 == 0:
                clear = 1
            else:
                clear = 0
            enable = 1 if rng.random() < 0.85 else 0
            start = 1 if rng.random() < 0.35 else 0
            mode = 1 if rng.random() < 0.5 else 0
            a = rng.randrange(256)
            b = rng.randrange(256)
            if i % 53 == 0:
                enable = 0
                start = 0
        row = {
            'i_rst_n': rst_n,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        if i >= 3 and rng.random() < 0.3:
            mid = {}
            if rng.random() < 0.5:
                mid['i_operand_a'] = rng.randrange(256)
            if rng.random() < 0.5:
                mid['i_operand_b'] = rng.randrange(256)
            if rng.random() < 0.2:
                mid['i_enable'] = 1 if rng.random() < 0.5 else 0
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows
