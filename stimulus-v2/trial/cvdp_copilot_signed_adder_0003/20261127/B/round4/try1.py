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
            clear = 1 if r < 0.02 else 0
            phase = i % 40
            if phase == 0:
                start = 1
                enable = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif phase in (1, 2, 3, 4):
                start = 0
                enable = 1
            else:
                start = 0
                enable = 0
                if rng.random() < 0.3:
                    a = rng.randint(0, 255)
                    b = rng.randint(0, 255)
                    mode = rng.randint(0, 1)
        row = {
            'i_rst_n': rst_n & 1,
            'i_start': start & 1,
            'i_enable': enable & 1,
            'i_mode': mode & 1,
            'i_clear': clear & 1,
            'i_operand_a': a & 0xFF,
            'i_operand_b': b & 0xFF,
        }
        rows.append(row)
    return rows
