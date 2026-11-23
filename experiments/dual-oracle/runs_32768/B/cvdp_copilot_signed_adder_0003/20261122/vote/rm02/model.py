def reference(vectors):
    IDLE, LOAD, COMPUTE, OUTPUT = 0, 1, 2, 3
    state = IDLE
    a_reg = b_reg = 0
    result = overflow = 0
    outs = []

    for idx, row in enumerate(vectors):
        rst = row.get('i_rst_n', 1)
        clr = row.get('i_clear', 0)
        held = False

        if rst == 0 or clr == 1:
            state = IDLE
            a_reg = b_reg = 0
            result = overflow = 0
            held = True

        outs.append({
            'o_resultant_sum': result & 0xFF,
            'o_overflow': overflow & 1,
            'o_ready': 1 if state == OUTPUT else 0,
            'o_status': state & 3
        })

        posedge = (idx % 2 == 0)
        if posedge and not held:
            if state == IDLE:
                if row.get('i_enable', 0) and row.get('i_start', 0):
                    state = LOAD
            elif state == LOAD:
                a_reg = row.get('i_operand_a', 0) & 0xFF
                b_reg = row.get('i_operand_b', 0) & 0xFF
                state = COMPUTE
            elif state == COMPUTE:
                a_s = a_reg - 256 if a_reg >= 128 else a_reg
                b_s = b_reg - 256 if b_reg >= 128 else b_reg
                if row.get('i_mode', 0):
                    val = a_s - b_s
                else:
                    val = a_s + b_s
                result = val & 0xFF
                overflow = 1 if val < -128 or val > 127 else 0
                state = OUTPUT
            elif state == OUTPUT:
                state = IDLE

    return outs
