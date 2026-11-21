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
            start = 1
            enable = 1
            mode = 0
            a = rng.randrange(256)
            b = rng.randrange(256)
        elif i == 4:
            start = 0
        elif i == 5:
            enable = 1
        elif i == 6:
            enable = 1
        elif i == 7:
            enable = 1
        elif i == 8:
            enable = 0
        elif i == 9:
            enable = 1
            start = 1
            mode = 1
            a = rng.randrange(256)
            b = rng.randrange(256)
        elif i == 10:
            start = 0
        elif i == 11:
            enable = 1
        elif i == 12:
            enable = 1
        elif i == 13:
            enable = 1
        elif i == 14:
            enable = 0
        elif i == 15:
            clear = 1
        elif i == 16:
            clear = 0
        elif i == 17:
            enable = 1
            start = 1
            mode = 0
            a = 0x7F
            b = 0x01
        elif i == 18:
            start = 0
        elif i == 19:
            enable = 1
        elif i == 20:
            enable = 1
        elif i == 21:
            enable = 1
        elif i == 22:
            enable = 0
        elif i == 23:
            enable = 1
            start = 1
            mode = 1
            a = 0x80
            b = 0x01
        elif i == 24:
            start = 0
        elif i == 25:
            enable = 1
        elif i == 26:
            enable = 1
        elif i == 27:
            enable = 1
        elif i == 28:
            enable = 0
        elif i >= 29:
            if i % 7 == 0:
                start = 1
                enable = 1
                mode = rng.randrange(2)
                a = rng.randrange(256)
                b = rng.randrange(256)
            elif i % 7 == 1:
                start = 0
            elif i % 7 == 2:
                enable = 1
            elif i % 7 == 3:
                enable = 1
            elif i % 7 == 4:
                enable = 1
            elif i % 7 == 5:
                enable = 0
            else:
                if rng.randrange(10) == 0:
                    clear = 1
                else:
                    clear = 0
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
