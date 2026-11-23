def reference(vectors):
    state = 0
    reg_a = 0
    reg_b = 0
    result = 0
    ov = 0
    prev = {
        'i_rst_n': 1,
        'i_start': 0,
        'i_enable': 0,
        'i_mode': 0,
        'i_clear': 0,
        'i_operand_a': 0,
        'i_operand_b': 0
    }
    outs = []
    for idx, row in enumerate(vectors):
        if isinstance(row, dict):
            for k in prev:
                if k in row:
                    prev[k] = row[k]
        elif isinstance(row, (list, tuple)):
            keys = ['i_rst_n', 'i_start', 'i_enable', 'i_mode', 'i_clear', 'i_operand_a', 'i_operand_b']
            for i, k in enumerate(keys):
                if i < len(row):
                    prev[k] = row[i]

        rst_n = prev['i_rst_n'] & 1
        start = prev['i_start'] & 1
        enable = prev['i_enable'] & 1
        mode = prev['i_mode'] & 1
        clear = prev['i_clear'] & 1
        a = prev['i_operand_a'] & 255
        b = prev['i_operand_b'] & 255

        if rst_n == 0:
            state = 0
            reg_a = 0
            reg_b = 0
            result = 0
            ov = 0
        elif clear == 1:
            state = 0
            result = 0
            ov = 0

        edge = None
        if isinstance(row, dict):
            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    if 'pos' in e.lower():
                        edge = 1
                    elif 'neg' in e.lower():
                        edge = 0
                else:
                    edge = 1 if e else 0
            elif 'i_clk' in row:
                edge = 1 if (row['i_clk'] & 1) else 0
        if edge is None:
            edge = 1 if (idx % 2 == 0) else 0

        outs.append({
            'o_resultant_sum': result & 255,
            'o_overflow': ov & 1,
            'o_ready': 1 if state == 3 else 0,
            'o_status': state & 3
        })

        if rst_n == 0 or clear == 1:
            state = 0
            result = 0
            ov = 0
            continue

        if edge == 1:
            if state == 0:
                if enable == 1 and start == 1:
                    state = 1
            elif state == 1:
                reg_a = a
                reg_b = b
                state = 2
            elif state == 2:
                sa = reg_a - 256 if reg_a >= 128 else reg_a
                sb = reg_b - 256 if reg_b >= 128 else reg_b
                if mode == 0:
                    full = sa + sb
                else:
                    full = sa - sb
                res_u = full & 255
                sres = res_u - 256 if res_u >= 128 else res_u
                if mode == 0:
                    if (sa >= 0 and sb >= 0 and sres < 0) or (sa < 0 and sb < 0 and sres >= 0):
                        ov_new = 1
                    else:
                        ov_new = 0
                else:
                    if (sa >= 0 and sb < 0 and sres < 0) or (sa < 0 and sb >= 0 and sres >= 0):
                        ov_new = 1
                    else:
                        ov_new = 0
                result = res_u
                ov = ov_new
                state = 3
            elif state == 3:
                state = 0
    return outs
