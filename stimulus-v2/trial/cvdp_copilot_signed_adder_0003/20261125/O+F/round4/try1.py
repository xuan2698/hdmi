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
        mid = None
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
                start = 1
                enable = 1
                mode = 0
                clear = 0
                a = rng.randrange(256)
                b = rng.randrange(256)
                mid = {'i_start': 0, 'i_enable': 0}
            elif i == 4:
                start = 1
                enable = 1
                mode = 1
                clear = 0
                a = rng.randrange(256)
                b = rng.randrange(256)
                mid = {'i_start': 0, 'i_enable': 0, 'i_operand_a': 0, 'i_operand_b': 0}
            elif i == 5:
                start = 1
                enable = 1
                mode = 0
                clear = 0
                a = 0
                b = 0
                mid = {'i_enable': 0}
            elif i == 6:
                start = 1
                enable = 0
                mode = 0
                clear = 0
                a = 0
                b = 0
            elif i == 7:
                start = 0
                enable = 1
                mode = 0
                clear = 0
                a = 0
                b = 0
            elif i == 8:
                start = 1
                enable = 1
                mode = 1
                clear = 0
                a = 0x80
                b = 0x01
                mid = {'i_start': 0}
            elif i == 9:
                start = 0
                enable = 1
                mode = 1
                clear = 0
                a = 0x80
                b = 0x01
            elif i == 10:
                start = 0
                enable = 1
                mode = 1
                clear = 0
                a = 0x80
                b = 0x01
            elif i == 11:
                start = 0
                enable = 1
                mode = 1
                clear = 0
                a = 0x80
                b = 0x01
            elif i == 12:
                start = 0
                enable = 0
                mode = 1
                clear = 0
                a = 0x80
                b = 0x01
            elif i == 13:
                start = 0
                enable = 0
                mode = 0
                clear = 1
                a = 0
                b = 0
            elif i == 14:
                start = 0
                enable = 0
                mode = 0
                clear = 0
                a = 0
                b = 0
            elif i == 15:
                start = 1
                enable = 1
                mode = 0
                clear = 0
                a = 0x7F
                b = 0x01
                mid = {'i_start': 0}
            elif i == 16:
                start = 0
                enable = 1
                mode = 0
                clear = 0
                a = 0x7F
                b = 0x01
            elif i == 17:
                start = 0
                enable = 1
                mode = 0
                clear = 0
                a = 0x7F
                b = 0x01
            elif i == 18:
                start = 0
                enable = 1
                mode = 0
                clear = 0
                a = 0x7F
                b = 0x01
            elif i == 19:
                start = 0
                enable = 0
                mode = 0
                clear = 0
                a = 0x7F
                b = 0x01
            elif i == 20:
                start = 1
                enable = 1
                mode = 1
                clear = 0
                a = 0x80
                b = 0x01
                mid = {'i_start': 0}
            elif i == 21:
                start = 0
                enable = 1
                mode = 1
                clear = 0
                a = 0x80
                b = 0x01
            elif i == 22:
                start = 0
                enable = 1
                mode = 1
                clear = 0
                a = 0x80
                b = 0x01
            elif i == 23:
                start = 0
                enable = 1
                mode = 1
                clear = 0
                a = 0x80
                b = 0x01
            elif i == 24:
                start = 0
                enable = 0
                mode = 1
                clear = 0
                a = 0x80
                b = 0x01
            else:
                phase = (i - 25) % 8
                if phase == 0:
                    start = 1
                    enable = 1
                    mode = rng.randrange(2)
                    clear = 0
                    a = rng.randrange(256)
                    b = rng.randrange(256)
                    mid = {'i_start': 0}
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
                    enable = 0
                elif phase == 6:
                    if rng.randrange(8) == 0:
                        clear = 1
                    else:
                        clear = 0
                else:
                    clear = 0
        row = {
            'i_rst_n': rst_n,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        if mid is not None:
            row['mid'] = mid
        rows.append(row)
    return rows
