def reference(vectors):
    state = 0
    cs_b = 1
    spi_clk = 0
    spi_data = 0
    bits_left = 16
    done = 0
    data_reg = 0
    result = []
    for idx, v in enumerate(vectors):
        def get_int(key, default=0):
            if not isinstance(v, dict):
                return default
            x = v.get(key, default)
            if isinstance(x, str):
                s = x.strip().lower()
                if s in ('1', 'true', 'high'):
                    return 1
                if s in ('0', 'false', 'low'):
                    return 0
                try:
                    return int(s, 0)
                except:
                    return default
            try:
                return int(x)
            except:
                return default
        i_rst_b = get_int('i_rst_b', 1)
        i_data_in = get_int('i_data_in', 0) & 0xFFFF
        i_enable = get_int('i_enable', 0) & 1
        i_fault = get_int('i_fault', 0) & 1
        i_clear = get_int('i_clear', 0) & 1
        is_pos = (idx % 2 == 0)
        if isinstance(v, dict):
            if 'edge' in v:
                e = str(v['edge']).lower()
                is_pos = ('pos' in e) or e in ('1', 'true')
            elif 'i_clk' in v:
                try:
                    is_pos = int(v['i_clk']) == 1
                except:
                    is_pos = str(v['i_clk']).lower() in ('1', 'true', 'posedge')
            elif 'clk' in v:
                try:
                    is_pos = int(v['clk']) == 1
                except:
                    is_pos = str(v['clk']).lower() in ('1', 'true', 'posedge')
        if i_rst_b == 0:
            state = 0
            cs_b = 1
            spi_clk = 0
            spi_data = 0
            bits_left = 16
            done = 0
            data_reg = 0
        result.append({
            'o_spi_cs_b': cs_b & 1,
            'o_spi_clk': spi_clk & 1,
            'o_spi_data': spi_data & 1,
            'o_bits_left': bits_left & 0x1F,
            'o_done': done & 1,
            'o_fsm_state': state & 3
        })
        if is_pos and i_rst_b != 0:
            if i_clear:
                n_state = 0
                n_cs = 1
                n_clk = 0
                n_data = 0
                n_bits = 16
                n_done = 0
                n_data_reg = 0
            elif i_enable == 0:
                n_state = 0
                n_cs = 1
                n_clk = 0
                n_data = 0
                n_bits = 16
                n_done = 0
                n_data_reg = 0
            elif i_fault:
                if state != 3:
                    n_state = 3
                    n_cs = 1
                    n_clk = 0
                    n_data = 0
                    n_bits = 16
                    n_done = 1
                    n_data_reg = 0
                else:
                    n_state = 3
                    n_cs = 1
                    n_clk = 0
                    n_data = 0
                    n_bits = 16
                    n_done = 0
                    n_data_reg = 0
            else:
                n_state = state
                n_cs = cs_b
                n_clk = spi_clk
                n_data = spi_data
                n_bits = bits_left
                n_done = 0
                n_data_reg = data_reg
                if state == 0:
                    n_cs = 1
                    n_clk = 0
                    n_data = 0
                    n_bits = 16
                    n_done = 0
                    if i_enable:
                        n_state = 1
                        n_cs = 0
                        n_data_reg = i_data_in
                elif state == 1:
                    n_cs = 0
                    n_clk = 0
                    n_data = (data_reg >> 15) & 1
                    n_data_reg = (data_reg << 1) & 0xFFFF
                    n_state = 2
                elif state == 2:
                    n_cs = 0
                    n_clk = 1
                    n_data = spi_data
                    if bits_left > 0:
                        n_bits = bits_left - 1
                    else:
                        n_bits = 0
                    if bits_left == 1:
                        n_done = 1
                        n_state = 0
                    else:
                        n_done = 0
                        n_state = 1
                elif state == 3:
                    n_cs = 1
                    n_clk = 0
                    n_data = 0
                    n_bits = 16
                    n_done = 0
                    n_state = 3
                    n_data_reg = 0
                else:
                    n_state = 0
                    n_cs = 1
                    n_clk = 0
                    n_data = 0
                    n_bits = 16
                    n_done = 0
                    n_data_reg = 0
            state = n_state & 3
            cs_b = n_cs & 1
            spi_clk = n_clk & 1
            spi_data = n_data & 1
            bits_left = n_bits & 0x1F
            done = n_done & 1
            data_reg = n_data_reg & 0xFFFF
    return result
