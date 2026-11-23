def reference(vectors):
    state = 0
    result = 0
    overflow = 0
    op_a = 0
    op_b = 0
    out_list = []

    for idx, row in enumerate(vectors):
        edge = row.get('edge', None)
        if edge is None:
            edge = row.get('i_clk', None)
        if edge is None:
            posedge = (idx % 2 == 0)
        else:
            s = str(edge).lower()
            if 'posedge' in s or s == '1' or s == 'true':
                posedge = True
            elif 'negedge' in s or s == '0' or s == 'false':
                posedge = False
            else:
                posedge = (idx % 2 == 0)

        rst_n = int(row.get('i_rst_n', 1)) & 1
        clear = int(row.get('i_clear', 0)) & 1
        enable = int(row.get('i_enable', 0)) & 1
        start = int(row.get('i_start', 0)) & 1
        mode = int(row.get('i_mode', 0)) & 1
        a_in = int(row.get('i_operand_a', 0)) & 0xFF
        b_in = int(row.get('i_operand_b', 0)) & 0xFF

        if rst_n == 0:
            state = 0
            result = 0
            overflow = 0
            op_a = 0
            op_b = 0
        elif clear == 1:
            state = 0
            result = 0
            overflow = 0
            op_a = 0
            op_b = 0

        out_status = state & 3
        out_ready = 1 if state == 3 else 0
        out_sum = result & 0xFF
        out_ov = overflow & 1

        out_list.append({
            'o_resultant_sum': out_sum,
            'o_overflow': out_ov,
            'o_ready': out_ready,
            'o_status': out_status
        })

        if posedge and rst_n == 1 and clear == 0:
            if enable == 0:
                state = 0
            else:
                if state == 0:
                    if start == 1:
                        state = 1
                elif state == 1:
                    op_a = a_in
                    op_b = b_in
                    state = 2
                elif state == 2:
                    a_s = op_a - 256 if op_a >= 128 else op_a
                    b_s = op_b - 256 if op_b >= 128 else op_b

                    if mode == 0:
                        full = a_s + b_s
                    else:
                        full = a_s - b_s

                    result = full & 0xFF
                    overflow = 1 if (full < -128 or full > 127) else 0
                    state = 3
                elif state == 3:
                    state = 0

    return out_list
