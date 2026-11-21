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
        elif i == 4:
            rst_n = 1
            start = 0
            enable = 0
            mode = 0
            clear = 0
            a = 0
            b = 0
        else:
            rst_n = 1
            phase = (i - 5) % 12
            if phase == 0:
                clear = 0
                enable = 1
                start = 1
                mode = 0
                a = 0x7F
                b = 0x01
            elif phase == 1:
                clear = 0
                enable = 1
                start = 0
                mode = 0
                a = 0x80
                b = 0x80
            elif phase == 2:
                clear = 0
                enable = 1
                start = 0
                mode = 0
                a = 0xFF
                b = 0x01
            elif phase == 3:
                clear = 0
                enable = 1
                start = 1
                mode = 1
                a = 0x80
                b = 0x01
            elif phase == 4:
                clear = 0
                enable = 1
                start = 0
                mode = 1
                a = 0x7F
                b = 0xFF
            elif phase == 5:
                clear = 0
                enable = 1
                start = 0
                mode = 1
                a = 0x00
                b = 0x80
            elif phase == 6:
                clear = 1
                enable = 0
                start = 0
                mode = 0
                a = 0
                b = 0
            elif phase == 7:
                clear = 0
                enable = 0
                start = 1
                mode = 1
                a = 0x55
                b = 0xAA
            elif phase == 8:
                clear = 0
                enable = 1
                start = 1
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif phase == 9:
                clear = 0
                enable = 0
                start = 0
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            elif phase == 10:
                clear = 0
                enable = 1
                start = 0
                mode = rng.randint(0, 1)
                a = rng.randint(0, 255)
                b = rng.randint(0, 255)
            else:
                clear = 0
                enable = 1
                start = 1
                mode = rng.randint(0, 1)
                a = rng.choice([0x7F, 0x80, 0xFF, 0x00, 0x01])
                b = rng.choice([0x7F, 0x80, 0xFF, 0x00, 0x01])
        row = {
            'i_rst_n': rst_n,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        if rng.random() < 0.2:
            mid = {
                'i_start': rng.randint(0, 1),
                'i_enable': rng.randint(0, 1),
                'i_mode': rng.randint(0, 1),
                'i_clear': 0 if rng.random() < 0.9 else 1,
                'i_operand_a': rng.randint(0, 255),
                'i_operand_b': rng.randint(0, 255),
            }
            row['mid'] = mid
        rows.append(row)
    return rows
