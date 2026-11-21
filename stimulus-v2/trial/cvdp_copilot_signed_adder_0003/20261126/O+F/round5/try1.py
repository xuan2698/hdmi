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
            if i == 3:
                start = 1; enable = 1; mode = 0; clear = 0; a = 0x7F; b = 0x01
            elif i == 4:
                start = 0; enable = 1; mode = 0; clear = 0; a = 0x7F; b = 0x01
            elif i == 5:
                start = 0; enable = 1; mode = 0; clear = 0; a = 0x7F; b = 0x01
            elif i == 6:
                start = 0; enable = 1; mode = 0; clear = 0; a = 0x7F; b = 0x01
            elif i == 7:
                start = 1; enable = 1; mode = 1; clear = 0; a = 0x80; b = 0x01
            elif i == 8:
                start = 0; enable = 1; mode = 1; clear = 0; a = 0x80; b = 0x01
            elif i == 9:
                start = 0; enable = 1; mode = 1; clear = 0; a = 0x80; b = 0x01
            elif i == 10:
                start = 0; enable = 1; mode = 1; clear = 0; a = 0x80; b = 0x01
            elif i == 11:
                start = 1; enable = 1; mode = 0; clear = 0; a = 0x55; b = 0xAA
            elif i == 12:
                start = 0; enable = 1; mode = 0; clear = 0; a = 0x55; b = 0xAA
            elif i == 13:
                start = 0; enable = 1; mode = 0; clear = 0; a = 0x55; b = 0xAA
            elif i == 14:
                start = 0; enable = 1; mode = 0; clear = 0; a = 0x55; b = 0xAA
            elif i == 15:
                start = 0; enable = 0; mode = 0; clear = 1; a = 0x55; b = 0xAA
            elif i == 16:
                start = 0; enable = 0; mode = 0; clear = 0; a = 0x55; b = 0xAA
            elif i == 17:
                start = 1; enable = 1; mode = 1; clear = 0; a = 0x10; b = 0x20
            elif i == 18:
                start = 0; enable = 1; mode = 1; clear = 0; a = 0x10; b = 0x20
            elif i == 19:
                start = 0; enable = 1; mode = 1; clear = 0; a = 0x10; b = 0x20
            elif i == 20:
                start = 0; enable = 1; mode = 1; clear = 0; a = 0x10; b = 0x20
            elif i == 21:
                start = 0; enable = 0; mode = 1; clear = 0; a = 0x10; b = 0x20
            else:
                start = 1 if rng.random() < 0.05 else 0
                enable = 1 if rng.random() < 0.9 else 0
                mode = 0 if rng.random() < 0.5 else 1
                clear = 1 if rng.random() < 0.02 else 0
                a = rng.randrange(256)
                b = rng.randrange(256)
        rows.append({
            'i_rst_n': rst_n,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        })
    return rows
