def reference(vectors):
    IDLE = 0
    TRANSMIT = 1
    CLOCK_TOGGLE = 2
    ERROR = 3
    
    state = IDLE
    shift_reg = 0
    bits_left = 16
    done = 0
    prev_clk = 0
    results = []
    
    for idx, row in enumerate(vectors):
        rst_b = row.get('i_rst_b', 1)
        data_in = row.get('i_data_in', 0)
        enable = row.get('i_enable', 0)
        fault = row.get('i_fault', 0)
        clear = row.get('i_clear', 0)
        
        if rst_b == 0:
            state = IDLE
            shift_reg = 0
            bits_left = 16
            done = 0
        
        if 'i_clk' in row:
            cur_clk = row['i_clk']
            if cur_clk == 1 and prev_clk == 0:
                is_pos = True
            elif cur_clk == 0 and prev_clk == 1:
                is_pos = False
            else:
                is_pos = False
            prev_clk = cur_clk
        elif 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                is_pos = 'pos' in e.lower()
            else:
                is_pos = bool(e)
        else:
            is_pos = (idx % 2 == 0)
        
        if state == IDLE or state == ERROR:
            cs_b = 1
            spi_clk = 0
            spi_data = 0
        else:
            cs_b = 0
            spi_clk = 1 if state == CLOCK_TOGGLE else 0
            spi_data = (shift_reg >> 15) & 1
        
        results.append({
            'o_spi_cs_b': cs_b,
            'o_spi_clk': spi_clk,
            'o_spi_data': spi_data,
            'o_bits_left': bits_left,
            'o_done': done,
            'o_fsm_state': state
        })
        
        if is_pos:
            if rst_b == 0:
                state = IDLE
                shift_reg = 0
                bits_left = 16
                done = 0
            elif clear == 1:
                state = IDLE
                shift_reg = 0
                bits_left = 16
                done = 0
            elif state == ERROR:
                state = ERROR
                shift_reg = 0
                bits_left = 16
                done = 0
            elif fault == 1:
                state = ERROR
                shift_reg = 0
                bits_left = 16
                done = 1
            elif enable == 0:
                state = IDLE
                shift_reg = 0
                bits_left = 16
                done = 0
            else:
                if state == IDLE:
                    state = TRANSMIT
                    shift_reg = data_in & 0xFFFF
                    bits_left = 16
                    done = 0
                elif state == TRANSMIT:
                    state = CLOCK_TOGGLE
                    done = 0
                elif state == CLOCK_TOGGLE:
                    if bits_left == 1:
                        state = IDLE
                        shift_reg = 0
                        bits_left = 16
                        done = 1
                    else:
                        shift_reg = (shift_reg << 1) & 0xFFFF
                        bits_left -= 1
                        state = TRANSMIT
                        done = 0
                else:
                    state = IDLE
                    shift_reg = 0
                    bits_left = 16
                    done = 0
    
    return results
