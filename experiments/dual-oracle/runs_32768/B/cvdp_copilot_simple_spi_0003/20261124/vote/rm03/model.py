def reference(vectors):
    IDLE, TX, CLK, ERR = 0, 1, 2, 3
    state = IDLE
    cs = 1
    clk = 0
    dat = 0
    bits = 16
    done = 0
    sh = 0
    out = []
    for row in vectors:
        rst = row.get('i_rst_b', row.get('rst_b', 1))
        data_in = row.get('i_data_in', row.get('data_in', 0))
        enable = row.get('i_enable', row.get('enable', 0))
        fault = row.get('i_fault', row.get('fault', 0))
        clear = row.get('i_clear', row.get('clear', 0))
        edge = row.get('edge', None)
        if edge is None:
            edge = row.get('i_clk', row.get('clk', 0))
        if isinstance(edge, str):
            s = edge.lower()
            pos = ('pos' in s) or (s in ('p', '1', 'rise', 'rising'))
        else:
            pos = (edge == 1) or (edge is True)
        rst = int(rst) & 1
        data_in = int(data_in) & 0xFFFF
        enable = int(enable) & 1
        fault = int(fault) & 1
        clear = int(clear) & 1
        if rst == 0:
            state = IDLE
            cs = 1
            clk = 0
            dat = 0
            bits = 16
            done = 0
            sh = 0
        out.append({
            'o_spi_cs_b': cs & 1,
            'o_spi_clk': clk & 1,
            'o_spi_data': dat & 1,
            'o_bits_left': bits & 31,
            'o_done': done & 1,
            'o_fsm_state': state & 3
        })
        if pos and rst == 1:
            if clear:
                state = IDLE
                cs = 1
                clk = 0
                dat = 0
                bits = 16
                done = 0
                sh = 0
            elif fault:
                state = ERR
                cs = 1
                clk = 0
                dat = 0
                bits = 16
                done = 0
            elif state == ERR:
                cs = 1
                clk = 0
                dat = 0
                bits = 16
                done = 0
                state = ERR
            elif enable == 0:
                state = IDLE
                cs = 1
                clk = 0
                dat = 0
                bits = 16
                done = 0
                sh = 0
            else:
                if state == IDLE:
                    cs = 1
                    clk = 0
                    dat = 0
                    bits = 16
                    done = 0
                    state = TX
                    sh = data_in
                elif state == TX:
                    cs = 0
                    dat = (sh >> 15) & 1
                    sh = (sh << 1) & 0xFFFF
                    done = 0
                    state = CLK
                elif state == CLK:
                    old_bits = bits
                    clk = 1 - clk
                    bits = (bits - 1) & 31
                    if old_bits == 1:
                        done = 1
                        state = IDLE
                    else:
                        done = 0
                        state = TX
    return out
