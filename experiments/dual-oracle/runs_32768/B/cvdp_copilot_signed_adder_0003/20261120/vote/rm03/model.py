def reference(vectors):
    state = 0
    reg_a = 0
    reg_b = 0
    result = 0
    overflow = 0
    ready = 0
    out_list = []
    for idx, row in enumerate(vectors):
        rst_n = row.get('i_rst_n', 1)
        if rst_n == 0:
            state = 0
            reg_a = 0
            reg_b = 0
            result = 0
            overflow = 0
            ready = 0
        out_list.append({
            'o_resultant_sum': result & 0xFF,
            'o_overflow': overflow & 1,
            'o_ready': ready & 1,
            'o_status': state & 3
        })
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                pos = ('pos' in e.lower() or 'rise' in e.lower())
            else:
                pos = (e == 1 or e is True)
        elif 'i_clk' in row:
            pos = (row['i_clk'] == 1)
        else:
            pos = (idx % 2 == 0)
        if rst_n == 0:
            continue
        if pos:
            i_clear = row.get('i_clear', 0)
            if i_clear == 1:
                state = 0
                reg_a = 0
                reg_b = 0
                result = 0
                overflow = 0
                ready = 0
            else:
                i_enable = row.get('i_enable', 0)
                if i_enable == 0:
                    state = 0
                    ready = 0
                else:
                    if state == 0:
                        ready = 0
                        i_start = row.get('i_start', 0)
                        if i_start == 1:
                            state = 1
                    elif state == 1:
                        reg_a = row.get('i_operand_a', 0) & 0xFF
                        reg_b = row.get('i_operand_b', 0) & 0xFF
                        state = 2
                    elif state == 2:
                        a_val = reg_a
                        b_val = reg_b
                        a_signed = a_val - 0x100 if (a_val & 0x80) else a_val
                        b_signed = b_val - 0x100 if (b_val & 0x80) else b_val
                        i_mode = row.get('i_mode', 0)
                        if i_mode == 1:
                            val = a_signed - b_signed
                        else:
                            val = a_signed + b_signed
                        ov = 1 if (val < -128 or val > 127) else 0
                        result = val & 0xFF
                        overflow = ov
                        ready = 1
                        state = 3
                    elif state == 3:
                        ready = 0
                        state = 0
    return out_list
