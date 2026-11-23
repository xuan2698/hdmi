def reference(vectors):
    state = 0
    result = 0
    overflow = 0
    operand_a = 0
    operand_b = 0
    out = []
    for idx, row in enumerate(vectors):
        rst = row.get('i_rst_n', 1) & 1
        if rst == 0:
            state = 0
            result = 0
            overflow = 0
            operand_a = 0
            operand_b = 0
        o_status = state & 3
        o_ready = 1 if state == 3 else 0
        o_resultant_sum = result & 0xFF
        o_overflow = overflow & 1
        out.append({
            'o_resultant_sum': o_resultant_sum,
            'o_overflow': o_overflow,
            'o_ready': o_ready,
            'o_status': o_status
        })
        is_posedge = (idx % 2 == 0)
        if is_posedge and rst != 0:
            if row.get('i_clear', 0) & 1:
                state = 0
                result = 0
                overflow = 0
            else:
                if state == 0:
                    if (row.get('i_enable', 0) & 1) and (row.get('i_start', 0) & 1):
                        state = 1
                    else:
                        state = 0
                elif state == 1:
                    operand_a = row.get('i_operand_a', 0) & 0xFF
                    operand_b = row.get('i_operand_b', 0) & 0xFF
                    state = 2
                elif state == 2:
                    a = operand_a
                    b = operand_b
                    mode = row.get('i_mode', 0) & 1
                    if mode == 0:
                        res = (a + b) & 0xFF
                        sa = (a >> 7) & 1
                        sb = (b >> 7) & 1
                        sr = (res >> 7) & 1
                        ov = 1 if (sa == sb and sr != sa) else 0
                    else:
                        res = (a - b) & 0xFF
                        sa = (a >> 7) & 1
                        sb = (b >> 7) & 1
                        sr = (res >> 7) & 1
                        ov = 1 if (sa != sb and sr != sa) else 0
                    result = res
                    overflow = ov
                    state = 3
                elif state == 3:
                    state = 0
    return out
