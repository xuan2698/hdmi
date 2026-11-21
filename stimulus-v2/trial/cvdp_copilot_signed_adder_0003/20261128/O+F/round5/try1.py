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
            clear = 1 if (i % 503 == 0) else 0
            enable = 0 if (i % 211) < 9 else 1
            start = 1 if (i % 31) == 0 else 0
            mode = (i // 19) & 1
            a = (i * 37 + 11) & 0xFF
            b = (i * 53 + 7) & 0xFF
            if i % 97 == 0:
                a = 0x80
                b = 0x80
            elif i % 89 == 0:
                a = 0x7F
                b = 0x7F
            elif i % 83 == 0:
                a = 0xFF
                b = 0x01
            elif i % 79 == 0:
                a = 0x00
                b = 0xFF
            elif i % 73 == 0:
                a = 0x7F
                b = 0x01
        row = {
            'i_rst_n': rst_n,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        if i >= 3 and (i % 41) == 0:
            row['mid'] = {
                'i_operand_a': (a + 1) & 0xFF,
                'i_operand_b': (b + 2) & 0xFF,
            }
        elif i >= 3 and (i % 29) == 0:
            row['mid'] = {
                'i_start': 0,
                'i_enable': 0,
            }
        rows.append(row)
    return rows
