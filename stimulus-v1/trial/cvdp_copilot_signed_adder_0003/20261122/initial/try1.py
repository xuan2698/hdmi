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
        elif i == 3:
            rst_n = 1
            start = 0
            enable = 0
            mode = 0
            clear = 0
            a = 0
            b = 0
        else:
            r = rng.random()
            if r < 0.05:
                clear = 1
                start = 0
                enable = 0
            elif r < 0.10:
                clear = 0
                enable = 0
                start = rng.randint(0, 1)
            elif r < 0.20:
                clear = 0
                enable = 1
                start = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.30:
                clear = 0
                enable = 1
                start = 0
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif r < 0.40:
                clear = 0
                enable = 0
                start = 0
            else:
                clear = 0
                enable = 1
                start = 1
                mode = rng.randint(0, 1)
                if rng.random() < 0.3:
                    a = rng.choice([0, 127, 128, 255, 1, 254])
                    b = rng.choice([0, 127, 128, 255, 1, 254])
                else:
                    a = rng.randint(0, 255)
                    b = rng.randint(0, 255)
        row = {
            'i_rst_n': rst_n,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        mid = {
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        row['mid'] = mid
        rows.append(row)
    return rows
