def reference(vectors):
    IDLE = 0
    LOAD = 1
    COMPUTE = 2
    OUTPUT = 3
    state = IDLE
    result = 0
    overflow = 0
    operand_a = 0
    operand_b = 0
    out = []
    for idx, row in enumerate(vectors):
        rst = row.get('i_rst_n', 1) & 1
        if rst == 0:
            state = IDLE
            result = 0
            overflow = 0
            operand_a = 0
            operand_b = 0
        o_status = state & 3
        o_ready = 1 if state == OUTPUT else 0
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
                state = IDLE
                result = 0
                overflow = 0
            elif (row.get('i_enable', 0) & 1) == 0:
                state = IDLE
            else:
                if state == IDLE:
                    if (row.get('i_start', 0) & 1):
                        state = LOAD
                    else:
                        state = IDLE
                elif state == LOAD:
                    operand_a = row.get('i_operand_a', 0) & 0xFF
                    operand_b = row.get('i_operand_b', 0) & 0xFF
                    state = COMPUTE
                elif state == COMPUTE:
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
                    state = OUTPUT
                elif state == OUTPUT:
                    state = IDLE
    return out
