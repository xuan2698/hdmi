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
        elif i == 2:
            rst_n = 1
        if i >= 2:
            r = rng.random()
            clear = 1 if r < 0.015 else 0
            start = 1 if rng.random() < 0.18 else 0
            enable = 1 if rng.random() < 0.88 else 0
            mode = 0 if rng.random() < 0.5 else 1
            if rng.random() < 0.45:
                a = rng.randrange(256)
            if rng.random() < 0.45:
                b = rng.randrange(256)
            if i % 97 == 0:
                a = 0x7F
                b = 0x01
            elif i % 97 == 1:
                a = 0x80
                b = 0xFF
            elif i % 97 == 2:
                a = 0x7F
                b = 0x7F
            elif i % 97 == 3:
                a = 0x80
                b = 0x80
        row = {
            'i_rst_n': rst_n,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        mid = {}
        if i >= 2:
            if rng.random() < 0.12:
                mid['i_start'] = rng.randrange(2)
            if rng.random() < 0.12:
                mid['i_enable'] = rng.randrange(2)
            if rng.random() < 0.12:
                mid['i_mode'] = rng.randrange(2)
            if rng.random() < 0.04:
                mid['i_clear'] = rng.randrange(2)
            if rng.random() < 0.18:
                mid['i_operand_a'] = rng.randrange(256)
            if rng.random() < 0.18:
                mid['i_operand_b'] = rng.randrange(256)
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows
