def reference(vectors):
    state = 0
    a_reg = 0
    b_reg = 0
    result = 0
    overflow = 0
    outs = []
    for idx, row in enumerate(vectors):
        def get(k, d=0):
            return row.get(k, d) if isinstance(row, dict) else d

        rst = get('i_rst_n', 1) & 1
        if rst == 0:
            state = 0
            a_reg = 0
            b_reg = 0
            result = 0
            overflow = 0

        ev = None
        if isinstance(row, dict):
            for k in ('edge', 'i_edge', 'clk_edge', 'edge_type'):
                if k in row:
                    ev = row[k]
                    break

        if ev is None:
            clk = get('i_clk', None)
            if clk is not None:
                if isinstance(clk, str):
                    is_pos = ('pos' in clk.lower())
                else:
                    is_pos = (clk == 1)
            else:
                is_pos = (idx % 2 == 0)
        else:
            if isinstance(ev, str):
                is_pos = ('pos' in ev.lower())
            else:
                is_pos = (ev == 1)

        outs.append({
            'o_resultant_sum': result & 0xff,
            'o_overflow': overflow & 1,
            'o_ready': 1 if state == 3 else 0,
            'o_status': state & 3
        })

        if is_pos and rst != 0:
            clear = get('i_clear', 0) & 1
            enable = get('i_enable', 0) & 1
            start = get('i_start', 0) & 1
            mode = get('i_mode', 0) & 1

            if clear:
                state = 0
                a_reg = 0
                b_reg = 0
                result = 0
                overflow = 0
            else:
                if state == 0:
                    if enable and start:
                        state = 1
                elif state == 1:
                    a_reg = get('i_operand_a', 0) & 0xff
                    b_reg = get('i_operand_b', 0) & 0xff
                    state = 2
                elif state == 2:
                    sa = a_reg - 256 if (a_reg & 0x80) else a_reg
                    sb = b_reg - 256 if (b_reg & 0x80) else b_reg
                    full = (sa - sb) if mode else (sa + sb)
                    res_u = full & 0xff
                    a_sign = (a_reg >> 7) & 1
                    b_sign = (b_reg >> 7) & 1
                    r_sign = (res_u >> 7) & 1
                    if mode:
                        overflow = 1 if (a_sign != b_sign and r_sign != a_sign) else 0
                    else:
                        overflow = 1 if (a_sign == b_sign and r_sign != a_sign) else 0
                    result = res_u
                    state = 3
                elif state == 3:
                    state = 0

    return outs
