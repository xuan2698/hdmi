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
            start = 0; enable = 0; clear = 0; mode = 0; a = 0; b = 0
        else:
            rst_n = 1
            if i == 3:
                start = 0; enable = 0; clear = 0; mode = 0; a = 0; b = 0
            else:
                r = rng.random()
                if r < 0.02:
                    clear = 1
                else:
                    clear = 0
                if rng.random() < 0.15:
                    start = 1
                else:
                    start = 0
                if rng.random() < 0.85:
                    enable = 1
                else:
                    enable = 0
                if rng.random() < 0.5:
                    mode = 1
                else:
                    mode = 0
                if rng.random() < 0.6:
                    a = rng.randrange(256)
                    b = rng.randrange(256)
        row = {
            'i_rst_n': rst_n & 1,
            'i_start': start & 1,
            'i_enable': enable & 1,
            'i_mode': mode & 1,
            'i_clear': clear & 1,
            'i_operand_a': a & 255,
            'i_operand_b': b & 255,
        }
        rows.append(row)
    return rows
