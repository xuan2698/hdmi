def reference(vectors):
    state = 0
    opa = 0
    opb = 0
    res = 0
    ovf = 0
    out = []
    for idx, row in enumerate(vectors):
        rst = row.get('i_rst_n', 1)
        if rst == 0:
            state = 0
            opa = 0
            opb = 0
            res = 0
            ovf = 0
        if 'edge' in row:
            e = row['edge']
            pos = (e == 1 or e == '1' or e == 'posedge' or e == 'pos' or e is True)
        else:
            c = row.get('i_clk', None)
            if c is None:
                pos = (idx % 2 == 0)
            else:
                pos = (c == 1 or c == '1' or c is True)
        ready = 1 if state == 3 else 0
        out.append({
            'o_resultant_sum': res & 0xFF,
            'o_overflow': 1 if ovf else 0,
            'o_ready': ready,
            'o_status': state & 3
        })
        if pos and rst != 0:
            if row.get('i_clear', 0):
                state = 0
                opa = 0
                opb = 0
                res = 0
                ovf = 0
            else:
                if state == 0:
                    if row.get('i_enable', 0) and row.get('i_start', 0):
                        state = 1
                elif state == 1:
                    opa = row.get('i_operand_a', 0) & 0xFF
                    opb = row.get('i_operand_b', 0) & 0xFF
                    state = 2
                elif state == 2:
                    a = opa - 256 if (opa & 0x80) else opa
                    b = opb - 256 if (opb & 0x80) else opb
                    if row.get('i_mode', 0):
                        m = a - b
                    else:
                        m = a + b
                    res = m & 0xFF
                    ovf = 1 if (m < -128 or m > 127) else 0
                    state = 3
                elif state == 3:
                    state = 0
    return out
