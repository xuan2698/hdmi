def reference(vectors):
    state = 0
    cs = 1
    clk = 0
    data = 0
    bits_left = 16
    done = 0
    shift_reg = 0
    prev_clk = 0
    row_count = 0
    out = []
    for row in vectors:
        i_rst_b = row.get('i_rst_b', 1)
        i_data_in = row.get('i_data_in', 0) & 0xFFFF
        i_enable = row.get('i_enable', 1)
        i_fault = row.get('i_fault', 0)
        i_clear = row.get('i_clear', 0)
        edge = row.get('edge', None)
        if edge is not None:
            if isinstance(edge, str):
                e = edge.lower()
                is_pos = ('pos' in e) or (e == 'p') or (e == '1')
            else:
                is_pos = (edge == 1 or edge is True)
        elif 'i_clk' in row:
            cur_clk = row['i_clk']
            is_pos = (cur_clk == 1 and prev_clk == 0)
            prev_clk = cur_clk
        else:
            is_pos = (row_count % 2 == 0)
        if i_rst_b == 0:
            state = 0
            cs = 1
            clk = 0
            data = 0
            bits_left = 16
            done = 0
            shift_reg = 0
        out.append({
            'o_spi_cs_b': cs,
            'o_spi_clk': clk,
            'o_spi_data': data,
            'o_bits_left': bits_left & 0x1F,
            'o_done': done,
            'o_fsm_state': state & 0x3
        })
        if is_pos and i_rst_b == 1:
            if i_clear:
                next_state = 0
                next_cs = 1
                next_clk = 0
                next_data = 0
                next_bits_left = 16
                next_done = 0
                next_shift_reg = shift_reg
            elif state == 3:
                next_state = 3
                next_cs = 1
                next_clk = 0
                next_data = 0
                next_bits_left = 16
                next_done = 0
                next_shift_reg = shift_reg
            elif i_fault:
                next_state = 3
                next_cs = 1
                next_clk = 0
                next_data = 0
                next_bits_left = 16
                next_done = 0
                next_shift_reg = shift_reg
            elif i_enable == 0:
                next_state = 0
                next_cs = 1
                next_clk = 0
                next_data = 0
                next_bits_left = 16
                next_done = 0
                next_shift_reg = shift_reg
            else:
                if state == 0:
                    next_state = 1
                    next_cs = 1
                    next_clk = 0
                    next_data = 0
                    next_bits_left = 16
                    next_done = 0
                    next_shift_reg = i_data_in
                elif state == 1:
                    next_state = 2
                    next_cs = 0
                    next_clk = clk
                    next_data = (shift_reg >> 15) & 1
                    next_bits_left = bits_left
                    next_done = 0
                    next_shift_reg = (shift_reg << 1) & 0xFFFF
                elif state == 2:
                    next_clk = 1 - clk
                    next_bits_left = (bits_left - 1) & 0x1F
                    if bits_left == 1:
                        next_state = 0
                        next_done = 1
                        next_cs = cs
                        next_data = data
                    else:
                        next_state = 1
                        next_done = 0
                        next_cs = cs
                        next_data = data
                    next_shift_reg = shift_reg
                else:
                    next_state = 0
                    next_cs = 1
                    next_clk = 0
                    next_data = 0
                    next_bits_left = 16
                    next_done = 0
                    next_shift_reg = shift_reg
            state = next_state
            cs = next_cs
            clk = next_clk
            data = next_data
            bits_left = next_bits_left
            done = next_done
            shift_reg = next_shift_reg
        row_count += 1
    return out
