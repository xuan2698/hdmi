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
        elif i == 3:
            rst_n = 1
        if i >= 3:
            r = rng.random()
            if r < 0.02:
                clear = 1
            else:
                clear = 0
            phase = i % 40
            if phase == 0:
                start = 1
                enable = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif phase == 1:
                start = 0
                enable = 1
            elif phase in (2, 3, 4):
                enable = 1
            else:
                start = 0
                enable = 0
                if rng.random() < 0.3:
                    a = rng.randint(0, 255)
                    b = rng.randint(0, 255)
                    mode = rng.randint(0, 1)
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
