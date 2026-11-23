def reference(vectors):
    state = 0
    a_reg = 0
    b_reg = 0
    sum_reg = 0
    ov_reg = 0
    cur_rst = 1
    cur_start = 0
    cur_enable = 0
    cur_mode = 0
    cur_clear = 0
    cur_a = 0
    cur_b = 0
    res = []
    idx = 0

    for row in vectors:
        edge = None
        if isinstance(row, dict):
            for k, v in row.items():
                lk = k.lower() if isinstance(k, str) else k
                if lk == 'i_rst_n' or lk == 'rst_n':
                    cur_rst = int(v) & 1
                elif lk == 'i_start' or lk == 'start':
                    cur_start = int(v) & 1
                elif lk == 'i_enable' or lk == 'enable':
                    cur_enable = int(v) & 1
                elif lk == 'i_mode' or lk == 'mode':
                    cur_mode = int(v) & 1
                elif lk == 'i_clear' or lk == 'clear':
                    cur_clear = int(v) & 1
                elif lk == 'i_operand_a' or lk == 'operand_a' or lk == 'a':
                    cur_a = int(v) & 0xFF
                elif lk == 'i_operand_b' or lk == 'operand_b' or lk == 'b':
                    cur_b = int(v) & 0xFF
            for ekey in ('edge', 'i_edge', 'clk_edge'):
                if ekey in row:
                    edge = row[ekey]
                    break
            if edge is None:
                if 'i_clk' in row:
                    edge = row['i_clk']
                elif 'clk' in row:
                    edge = row['clk']
                elif 'clock' in row:
                    edge = row['clock']
        elif isinstance(row, (list, tuple)):
            seq = list(row)
            if len(seq) == 8:
                edge = seq[0]
                cur_rst = int(seq[1]) & 1
                cur_start = int(seq[2]) & 1
                cur_enable = int(seq[3]) & 1
                cur_mode = int(seq[4]) & 1
                cur_clear = int(seq[5]) & 1
                cur_a = int(seq[6]) & 0xFF
                cur_b = int(seq[7]) & 0xFF
            elif len(seq) == 7:
                cur_rst = int(seq[0]) & 1
                cur_start = int(seq[1]) & 1
                cur_enable = int(seq[2]) & 1
                cur_mode = int(seq[3]) & 1
                cur_clear = int(seq[4]) & 1
                cur_a = int(seq[5]) & 0xFF
                cur_b = int(seq[6]) & 0xFF
            elif len(seq) > 0:
                edge = seq[0]

        if edge is None:
            edge_pos = (idx % 2 == 0)
        else:
            if isinstance(edge, str):
                e = edge.lower()
                if 'pos' in e or e == '1':
                    edge_pos = True
                elif 'neg' in e or e == '0':
                    edge_pos = False
                else:
                    edge_pos = (idx % 2 == 0)
            else:
                edge_pos = bool(edge)
        idx += 1

        if cur_rst == 0:
            state = 0
            a_reg = 0
            b_reg = 0
            sum_reg = 0
            ov_reg = 0

        out_status = state
        out_ready = 1 if state == 3 else 0
        out_sum = sum_reg & 0xFF
        out_ov = ov_reg & 1
        res.append({
            'o_resultant_sum': out_sum,
            'o_overflow': out_ov,
            'o_ready': out_ready,
            'o_status': out_status
        })

        if edge_pos:
            if cur_rst == 0:
                state = 0
                a_reg = 0
                b_reg = 0
                sum_reg = 0
                ov_reg = 0
            elif cur_clear == 1:
                state = 0
                a_reg = 0
                b_reg = 0
                sum_reg = 0
                ov_reg = 0
            elif cur_enable == 0:
                state = 0
            else:
                if state == 0:
                    if cur_start == 1:
                        state = 1
                elif state == 1:
                    a_reg = cur_a & 0xFF
                    b_reg = cur_b & 0xFF
                    state = 2
                elif state == 2:
                    a = a_reg if a_reg < 128 else a_reg - 256
                    b = b_reg if b_reg < 128 else b_reg - 256
                    if cur_mode == 0:
                        full = a + b
                    else:
                        full = a - b
                    sum_reg = full & 0xFF
                    ov_reg = 1 if (full < -128 or full > 127) else 0
                    state = 3
                elif state == 3:
                    state = 0

    return res
