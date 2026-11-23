def reference(vectors):
    state = 0
    cs = 1
    clk = 0
    data = 0
    bits = 16
    done = 0
    data_reg = 0
    prev_clk = None
    out = []

    for idx, row in enumerate(vectors):
        def getv(key, default=0):
            if isinstance(row, dict):
                val = row.get(key, default)
                try:
                    return int(val)
                except Exception:
                    return default
            return default

        rst = getv('i_rst_b', 1)
        fault = getv('i_fault', 0)
        clear = getv('i_clear', 0)
        enable = getv('i_enable', 0)
        din = getv('i_data_in', 0) & 0xFFFF

        current_clk = None
        if isinstance(row, dict) and 'i_clk' in row:
            try:
                current_clk = int(row['i_clk'])
            except Exception:
                current_clk = None

        is_pos = (idx % 2 == 0)
        explicit_edge = False
        if isinstance(row, dict):
            for k in ('edge', 'EDGE', 'Edge'):
                if k in row:
                    e = row[k]
                    explicit_edge = True
                    if isinstance(e, str):
                        el = e.lower()
                        if el.startswith('pos') or el == '1':
                            is_pos = True
                        elif el.startswith('neg') or el == '0':
                            is_pos = False
                        else:
                            try:
                                is_pos = bool(int(e))
                            except Exception:
                                is_pos = True
                    else:
                        try:
                            is_pos = bool(int(e))
                        except Exception:
                            is_pos = bool(e)
                    break

        if not explicit_edge and current_clk is not None and prev_clk is not None:
            if current_clk == 1 and prev_clk == 0:
                is_pos = True
            elif current_clk == 0 and prev_clk == 1:
                is_pos = False

        if rst == 0:
            state = 0
            cs = 1
            clk = 0
            data = 0
            bits = 16
            done = 0
            data_reg = 0

        out.append({
            'o_spi_cs_b': int(cs) & 1,
            'o_spi_clk': int(clk) & 1,
            'o_spi_data': int(data) & 1,
            'o_bits_left': int(bits) & 0x1F,
            'o_done': int(done) & 1,
            'o_fsm_state': int(state) & 0x3
        })

        if is_pos:
            if rst == 0:
                state = 0
                cs = 1
                clk = 0
                data = 0
                bits = 16
                done = 0
                data_reg = 0
            else:
                n_state = state
                n_cs = cs
                n_clk = clk
                n_data = data
                n_bits = bits
                n_done = 0
                n_data_reg = data_reg

                if fault:
                    if state != 3:
                        n_done = 1
                    else:
                        n_done = 0
                    n_state = 3
                    n_cs = 1
                    n_clk = 0
                    n_data = 0
                    n_bits = 16
                elif clear:
                    n_state = 0
                    n_cs = 1
                    n_clk = 0
                    n_data = 0
                    n_bits = 16
                    n_done = 0
                elif state == 3:
                    n_state = 3
                    n_cs = 1
                    n_clk = 0
                    n_data = 0
                    n_bits = 16
                    n_done = 0
                elif enable == 0:
                    n_state = 0
                    n_cs = 1
                    n_clk = 0
                    n_data = 0
                    n_bits = 16
                    n_done = 0
                else:
                    if state == 0:
                        n_cs = 1
                        n_clk = 0
                        n_data = 0
                        n_bits = 16
                        n_data_reg = din
                        n_cs = 0
                        n_state = 1
                    elif state == 1:
                        n_cs = 0
                        b = bits
                        if b < 1:
                            b = 1
                        if b > 16:
                            b = 16
                        n_data = (data_reg >> (b - 1)) & 1
                        n_state = 2
                    elif state == 2:
                        n_clk = 1 - clk
                        if bits == 1:
                            n_done = 1
                            n_state = 0
                            n_cs = 1
                            n_clk = 0
                            n_bits = 16
                        else:
                            n_bits = bits - 1
                            n_state = 1
                    else:
                        n_state = 3
                        n_cs = 1
                        n_clk = 0
                        n_data = 0
                        n_bits = 16
                        n_done = 0

                state = n_state
                cs = n_cs
                clk = n_clk
                data = n_data
                bits = n_bits
                done = n_done
                data_reg = n_data_reg

        if current_clk is not None:
            prev_clk = current_clk

    return out
