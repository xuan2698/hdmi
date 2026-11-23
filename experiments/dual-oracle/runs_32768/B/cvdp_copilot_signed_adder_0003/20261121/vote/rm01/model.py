def reference(vectors):
    def is_posedge(row, idx):
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                s = e.lower()
                return ('pos' in s) or s in ('1', 'p', 'rising')
            return bool(e)
        if 'i_clk' in row:
            e = row['i_clk']
            if isinstance(e, str):
                s = e.lower()
                return ('pos' in s) or s in ('1', 'p', 'rising')
            return e == 1 or e is True
        if 'clk' in row:
            e = row['clk']
            if isinstance(e, str):
                s = e.lower()
                return ('pos' in s) or s in ('1', 'p', 'rising')
            return e == 1 or e is True
        return idx % 2 == 0

    cur = {
        'i_rst_n': 1,
        'i_start': 0,
        'i_enable': 0,
        'i_mode': 0,
        'i_clear': 0,
        'i_operand_a': 0,
        'i_operand_b': 0,
    }

    state = 0
    reg_a = 0
    reg_b = 0
    result = 0
    overflow = 0
    outs = []

    for idx, row in enumerate(vectors):
        for name in cur:
            if name in row:
                cur[name] = row[name]

        if cur['i_rst_n'] == 0 or cur['i_rst_n'] is False:
            state = 0
            reg_a = 0
            reg_b = 0
            result = 0
            overflow = 0

        outs.append({
            'o_resultant_sum': result & 255,
            'o_overflow': overflow & 1,
            'o_ready': 1 if state == 3 else 0,
            'o_status': state & 3,
        })

        if is_posedge(row, idx):
            if not (cur['i_rst_n'] == 0 or cur['i_rst_n'] is False):
                if cur['i_clear'] == 1 or cur['i_clear'] is True:
                    state = 0
                    reg_a = 0
                    reg_b = 0
                    result = 0
                    overflow = 0
                else:
                    if state == 0:
                        if ((cur['i_enable'] == 1 or cur['i_enable'] is True) and
                                (cur['i_start'] == 1 or cur['i_start'] is True)):
                            state = 1
                    elif state == 1:
                        a_bits = int(cur['i_operand_a']) & 255
                        b_bits = int(cur['i_operand_b']) & 255
                        reg_a = a_bits - 256 if a_bits >= 128 else a_bits
                        reg_b = b_bits - 256 if b_bits >= 128 else b_bits
                        state = 2
                    elif state == 2:
                        if cur['i_mode'] == 1 or cur['i_mode'] is True:
                            full = reg_a - reg_b
                        else:
                            full = reg_a + reg_b
                        overflow = 1 if full < -128 or full > 127 else 0
                        result = full & 255
                        state = 3
                    elif state == 3:
                        state = 0

    return outs
