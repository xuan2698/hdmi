def reference(vectors):
    state = 0
    a_reg = 0
    b_reg = 0
    result = 0
    overflow = 0
    outputs = []

    for row in vectors:
        edge = row.get('edge', None)
        if edge is None:
            clk = row.get('i_clk', 1)
            posedge = (clk == 1 or clk == '1' or clk is True)
        else:
            if isinstance(edge, str):
                posedge = edge.lower().startswith('pos') or edge == '1'
            else:
                posedge = bool(edge)

        rst_n = row.get('i_rst_n', 1)
        start = row.get('i_start', 0)
        enable = row.get('i_enable', 0)
        mode = row.get('i_mode', 0)
        clear = row.get('i_clear', 0)
        opa = row.get('i_operand_a', 0) & 0xFF
        opb = row.get('i_operand_b', 0) & 0xFF

        if rst_n == 0:
            state = 0
            a_reg = 0
            b_reg = 0
            result = 0
            overflow = 0

        outputs.append({
            'o_resultant_sum': result & 0xFF,
            'o_overflow': overflow & 1,
            'o_ready': 1 if state == 3 else 0,
            'o_status': state & 3
        })

        if posedge:
            if rst_n == 0:
                state = 0
                a_reg = 0
                b_reg = 0
                result = 0
                overflow = 0
            elif clear:
                state = 0
                result = 0
                overflow = 0
            elif enable == 0:
                state = 0
            else:
                if state == 0:
                    if start:
                        state = 1
                elif state == 1:
                    a_reg = opa
                    b_reg = opb
                    state = 2
                elif state == 2:
                    av = a_reg - 256 if a_reg >= 128 else a_reg
                    bv = b_reg - 256 if b_reg >= 128 else b_reg
                    if mode == 1:
                        val = av - bv
                    else:
                        val = av + bv
                    result = val & 0xFF
                    overflow = 1 if (val < -128 or val > 127) else 0
                    state = 3
                elif state == 3:
                    state = 0

    return outputs
