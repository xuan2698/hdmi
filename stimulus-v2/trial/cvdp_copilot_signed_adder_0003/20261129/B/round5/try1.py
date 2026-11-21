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
        else:
            rst_n = 1
        if i == 3:
            start = 0; enable = 0; clear = 0; mode = 0; a = 0; b = 0
        elif i > 3:
            r = rng.random()
            clear = 1 if r < 0.02 else 0
            start = 1 if rng.random() < 0.15 else 0
            enable = 1 if rng.random() < 0.85 else 0
            mode = 1 if rng.random() < 0.5 else 0
            if rng.random() < 0.6:
                a = rng.randrange(256)
                b = rng.randrange(256)
        row = {
            'i_rst_n': rst_n,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        rows.append(row)
    return rows
