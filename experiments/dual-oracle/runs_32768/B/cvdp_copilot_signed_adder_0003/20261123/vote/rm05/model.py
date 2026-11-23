def reference(vectors):
    IDLE, LOAD, COMPUTE, OUTPUT = 0, 1, 2, 3
    W = 8
    MASK = (1 << W) - 1
    MINV = -(1 << (W - 1))
    MAXV = (1 << (W - 1)) - 1

    state = IDLE
    a_reg = 0
    b_reg = 0
    result = 0
    overflow = 0
    out = []

    for idx, row in enumerate(vectors):
        rst_n = row.get('i_rst_n', 1)
        start = row.get('i_start', 0)
        enable = row.get('i_enable', 1)
        mode = row.get('i_mode', 0)
        clear = row.get('i_clear', 0)
        opa = row.get('i_operand_a', 0) & MASK
        opb = row.get('i_operand_b', 0) & MASK

        if rst_n == 0:
            state = IDLE
            a_reg = 0
            b_reg = 0
            result = 0
            overflow = 0

        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                is_pos = ('pos' in e.lower()) or (e == '1')
            else:
                is_pos = (e == 1)
        elif 'i_clk' in row:
            is_pos = (row['i_clk'] == 1)
        elif 'clk' in row:
            is_pos = (row['clk'] == 1)
        else:
            is_pos = (idx % 2 == 0)

        out.append({
            'o_resultant_sum': result & MASK,
            'o_overflow': overflow & 1,
            'o_ready': 1 if state == OUTPUT else 0,
            'o_status': state
        })

        if is_pos:
            if rst_n == 0:
                pass
            elif clear == 1:
                state = IDLE
                a_reg = 0
                b_reg = 0
                result = 0
                overflow = 0
            elif enable == 0:
                state = IDLE
            else:
                if state == IDLE:
                    if start == 1:
                        state = LOAD
                elif state == LOAD:
                    a_reg = opa
                    b_reg = opb
                    state = COMPUTE
                elif state == COMPUTE:
                    sa = a_reg if a_reg < (1 << (W - 1)) else a_reg - (1 << W)
                    sb = b_reg if b_reg < (1 << (W - 1)) else b_reg - (1 << W)
                    if mode == 1:
                        s = sa - sb
                    else:
                        s = sa + sb
                    result = s & MASK
                    overflow = 1 if (s < MINV or s > MAXV) else 0
                    state = OUTPUT
                elif state == OUTPUT:
                    state = IDLE

    return out
