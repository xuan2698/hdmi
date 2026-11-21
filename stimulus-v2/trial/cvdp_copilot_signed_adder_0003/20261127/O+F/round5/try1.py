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
            clear = 1 if r < 0.02 else 0
            phase = i % 24
            if phase == 0:
                start = 1
                enable = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif phase == 1:
                start = 0
                enable = 1
            elif phase == 2:
                enable = 1
            elif phase == 3:
                enable = 1
            elif phase == 4:
                enable = 1
            elif phase == 5:
                enable = 1
            elif phase == 6:
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
        if i == 1:
            row['mid'] = {'i_start': 1, 'i_enable': 0, 'i_clear': 1}
        elif i == 2:
            row['mid'] = {'i_start': 0, 'i_enable': 0}
        elif i == 3:
            row['mid'] = {'i_start': 0, 'i_enable': 0, 'i_operand_a': 0, 'i_operand_b': 0}
        elif i == 4:
            row['mid'] = {'i_enable': 0}
        rows.append(row)
    return rows
