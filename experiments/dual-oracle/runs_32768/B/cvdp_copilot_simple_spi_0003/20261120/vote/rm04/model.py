def reference(vectors):
    state = 0
    cs_b = 1
    spi_clk = 0
    spi_data = 0
    bits_left = 16
    done = 0
    shift_reg = 0
    prev_clk = 0
    outputs = []
    for row_idx, row in enumerate(vectors):
        if isinstance(row, dict):
            edge = row.get('edge', None)
            i_clk = row.get('i_clk', None)
            i_rst_b = row.get('i_rst_b', 1)
            i_data_in = row.get('i_data_in', 0)
            i_enable = row.get('i_enable', 0)
            i_fault = row.get('i_fault', 0)
            i_clear = row.get('i_clear', 0)
        else:
            edge = None
            i_clk = None
            i_rst_b = 1
            i_data_in = 0
            i_enable = 0
            i_fault = 0
            i_clear = 0
            n = len(row)
            if n > 0 and isinstance(row[0], str):
                edge = row[0]
                if n > 1: i_rst_b = row[1]
                if n > 2: i_data_in = row[2]
                if n > 3: i_enable = row[3]
                if n > 4: i_fault = row[4]
                if n > 5: i_clear = row[5]
            elif n > 0 and isinstance(row[-1], str):
                edge = row[-1]
                if n > 0: i_rst_b = row[0]
                if n > 1: i_data_in = row[1]
                if n > 2: i_enable = row[2]
                if n > 3: i_fault = row[3]
                if n > 4: i_clear = row[4]
            elif n == 5:
                i_rst_b = row[0]
                i_data_in = row[1]
                i_enable = row[2]
                i_fault = row[3]
                i_clear = row[4]
            elif n >= 6:
                i_clk = row[0]
                i_rst_b = row[1]
                i_data_in = row[2]
                i_enable = row[3]
                i_fault = row[4]
                i_clear = row[5]
        if edge is not None:
            if isinstance(edge, str):
                posedge = edge.lower().startswith('pos')
            else:
                posedge = bool(edge)
        elif i_clk is not None:
            posedge = (prev_clk == 0 and i_clk == 1)
            prev_clk = i_clk
        else:
            posedge = (row_idx % 2 == 0)
        if i_rst_b == 0:
            state = 0
            cs_b = 1
            spi_clk = 0
            spi_data = 0
            bits_left = 16
            done = 0
            shift_reg = 0
        outputs.append({
            'o_spi_cs_b': cs_b,
            'o_spi_clk': spi_clk,
            'o_spi_data': spi_data,
            'o_bits_left': bits_left,
            'o_done': done,
            'o_fsm_state': state
        })
        if posedge and i_rst_b != 0:
            n_state = state
            n_cs_b = cs_b
            n_spi_clk = spi_clk
            n_spi_data = spi_data
            n_bits_left = bits_left
            n_done = done
            n_shift_reg = shift_reg
            if i_fault:
                n_state = 3
                n_cs_b = 1
                n_spi_clk = 0
                n_spi_data = 0
                n_bits_left = 16
                n_done = 0
                n_shift_reg = 0
            elif i_clear:
                n_state = 0
                n_cs_b = 1
                n_spi_clk = 0
                n_spi_data = 0
                n_bits_left = 16
                n_done = 0
                n_shift_reg = 0
            elif state != 3 and i_enable == 0:
                n_state = 0
                n_cs_b = 1
                n_spi_clk = 0
                n_spi_data = 0
                n_bits_left = 16
                n_done = 0
                n_shift_reg = 0
            else:
                if state == 0:
                    n_cs_b = 1
                    n_spi_clk = 0
                    n_spi_data = 0
                    n_bits_left = 16
                    n_done = 0
                    if i_enable:
                        n_state = 1
                        n_shift_reg = i_data_in
                    else:
                        n_state = 0
                elif state == 1:
                    n_cs_b = 0
                    n_spi_data = (shift_reg >> 15) & 1
                    n_shift_reg = (shift_reg << 1) & 0xFFFF
                    n_state = 2
                elif state == 2:
                    n_spi_clk = 1 - spi_clk
                    if bits_left > 1:
                        n_bits_left = bits_left - 1
                        n_state = 1
                    else:
                        n_bits_left = 16
                        n_done = 1
                        n_state = 0
                elif state == 3:
                    n_cs_b = 1
                    n_spi_clk = 0
                    n_spi_data = 0
                    n_bits_left = 16
                    n_done = 0
                    n_state = 3
            state = n_state
            cs_b = n_cs_b
            spi_clk = n_spi_clk
            spi_data = n_spi_data
            bits_left = n_bits_left
            done = n_done
            shift_reg = n_shift_reg
    return outputs
