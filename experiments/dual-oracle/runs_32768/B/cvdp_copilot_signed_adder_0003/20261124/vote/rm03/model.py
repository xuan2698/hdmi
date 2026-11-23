def reference(vectors):
    current = {
        'i_rst_n': 0,
        'i_start': 0,
        'i_enable': 0,
        'i_mode': 0,
        'i_clear': 0,
        'i_operand_a': 0,
        'i_operand_b': 0
    }
    state = 0
    a_reg = 0
    b_reg = 0
    result = 0
    overflow = 0
    outs = []
    keys = ('i_rst_n', 'i_start', 'i_enable', 'i_mode', 'i_clear', 'i_operand_a', 'i_operand_b')
    for idx, row in enumerate(vectors):
        for k in keys:
            if k in row:
                current[k] = int(row[k])
        pos = False
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                el = e.lower()
                pos = el.startswith('pos') or el == 'p' or el == '1'
            else:
                pos = bool(e)
        elif 'clk_edge' in row:
            e = row['clk_edge']
            if isinstance(e, str):
                el = e.lower()
                pos = el.startswith('pos') or el == 'p' or el == '1'
            else:
                pos = bool(e)
        elif 'i_clk' in row:
            pos = bool(int(row['i_clk']))
        else:
            pos = (idx % 2 == 0)
        if current['i_rst_n'] == 0:
            state = 0
            a_reg = 0
            b_reg = 0
            result = 0
            overflow = 0
        outs.append({
            'o_resultant_sum': result & 0xFF,
            'o_overflow': overflow & 1,
            'o_ready': 1 if state == 3 else 0,
            'o_status': state & 3
        })
        if pos and current['i_rst_n'] == 1:
            if current['i_clear'] == 1:
                state = 0
                result = 0
                overflow = 0
            else:
                if state == 0:
                    if current['i_enable'] == 1 and current['i_start'] == 1:
                        state = 1
                elif state == 1:
                    a_reg = current['i_operand_a'] & 0xFF
                    b_reg = current['i_operand_b'] & 0xFF
                    state = 2
                elif state == 2:
                    a_s = a_reg if a_reg < 128 else a_reg - 256
                    b_s = b_reg if b_reg < 128 else b_reg - 256
                    if current['i_mode'] == 1:
                        full = a_s - b_s
                    else:
                        full = a_s + b_s
                    result = full & 0xFF
                    overflow = 1 if (full < -128 or full > 127) else 0
                    state = 3
                elif state == 3:
                    state = 0
    return outs
