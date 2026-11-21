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
        else:
            rst_n = 1
            clear = 1 if (i % 500 == 0) else 0
            enable = 0 if (i % 200) < 10 else 1
            start = 1 if (i % 37) == 0 else 0
            mode = (i // 23) & 1
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
        row = {
            'i_rst_n': rst_n,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        if i >= 4 and (i % 41) == 0:
            row['mid'] = {
                'i_operand_a': (a + 1) & 0xFF,
                'i_operand_b': (b + 2) & 0xFF,
            }
        rows.append(row)
    return rows
