def reference(vectors):
    out = []
    state = 0
    cs = 1
    clk = 0
    data = 0
    bits = 16
    done = 0
    shift = 0
    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            rst = row.get('i_rst_b', 1)
            enable = row.get('i_enable', 0)
            fault = row.get('i_fault', 0)
            clear = row.get('i_clear', 0)
            data_in = row.get('i_data_in', 0)
        else:
            if len(row) == 5:
                rst, data_in, enable, fault, clear = row
            elif len(row) == 6:
                _, rst, data_in, enable, fault, clear = row
            else:
                rst = 1
                data_in = 0
                enable = 0
                fault = 0
                clear = 0
        pos = (i % 2 == 0)
        if rst == 0:
            state = 0
            cs = 1
            clk = 0
            data = 0
            bits = 16
            done = 0
            shift = 0
        out.append({
            'o_spi_cs_b': cs,
            'o_spi_clk': clk,
            'o_spi_data': data,
            'o_bits_left': bits,
            'o_done': done,
            'o_fsm_state': state
        })
        if pos and rst != 0:
            if clear:
                state = 0
                cs = 1
                clk = 0
                data = 0
                bits = 16
                done = 0
                shift = 0
            elif state == 3:
                cs = 1
                clk = 0
                data = 0
                bits = 16
                done = 0
            elif fault:
                state = 3
                cs = 1
                clk = 0
                data = 0
                bits = 16
                done = 1
                shift = 0
            elif not enable:
                state = 0
                cs = 1
                clk = 0
                data = 0
                bits = 16
                done = 0
                shift = 0
            else:
                if state == 0:
                    cs = 1
                    clk = 0
                    data = 0
                    bits = 16
                    done = 0
                    shift = data_in
                    cs = 0
                    state = 1
                elif state == 1:
                    data = (shift >> 15) & 1
                    shift = (shift << 1) & 0xFFFF
                    state = 2
                elif state == 2:
                    clk = 1 - clk
                    bits = bits - 1
                    if bits == 0:
                        done = 1
                        state = 0
                    else:
                        state = 1
    return out
