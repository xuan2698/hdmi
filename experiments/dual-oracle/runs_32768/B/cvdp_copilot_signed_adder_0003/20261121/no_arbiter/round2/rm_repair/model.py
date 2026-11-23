def reference(vectors):
    IDLE, LOAD, COMPUTE, OUTPUT = 0, 1, 2, 3
    state = IDLE
    a_reg = 0
    b_reg = 0
    res = 0
    ov = 0
    out = []

    for idx, row in enumerate(vectors):
        if isinstance(row, dict):
            edge_val = row.get('edge', None)

            def g(name):
                try:
                    return int(row.get(name, 0))
                except Exception:
                    return 0
        else:
            edge_val = None

            def g(name):
                return 0

        if edge_val is None:
            is_pos = (idx % 2 == 0)
        else:
            s = str(edge_val).lower()
            is_pos = ('posedge' in s) or s in ('pos', 'p', '1', 'rise')

        rst_n = g('i_rst_n')

        if rst_n == 0:
            state = IDLE
            a_reg = 0
            b_reg = 0
            res = 0
            ov = 0

        out.append({
            'o_resultant_sum': res & 0xFF,
            'o_overflow': ov & 1,
            'o_ready': 1 if state == OUTPUT else 0,
            'o_status': state & 3
        })

        if rst_n != 0 and is_pos:
            clear = g('i_clear')
            enable = g('i_enable')
            start = g('i_start')
            mode = g('i_mode')

            if clear:
                state = IDLE
                a_reg = 0
                b_reg = 0
                res = 0
                ov = 0
            elif not enable:
                state = IDLE
            else:
                if state == IDLE:
                    if start:
                        state = LOAD
                elif state == LOAD:
                    a_reg = g('i_operand_a') & 0xFF
                    b_reg = g('i_operand_b') & 0xFF
                    state = COMPUTE
                elif state == COMPUTE:
                    a = a_reg
                    b = b_reg

                    if mode == 0:
                        s = (a + b) & 0xFF
                        sa = (a >> 7) & 1
                        sb = (b >> 7) & 1
                        sr = (s >> 7) & 1
                        ov = 1 if (sa == sb and sr != sa) else 0
                        res = s
                    else:
                        d = (a - b) & 0xFF
                        sa = (a >> 7) & 1
                        sb = (b >> 7) & 1
                        sr = (d >> 7) & 1
                        ov = 1 if (sa != sb and sr != sa) else 0
                        res = d

                    state = OUTPUT
                elif state == OUTPUT:
                    state = IDLE

    return out
