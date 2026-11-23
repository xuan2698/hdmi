def reference(vectors):
    state = 0          # 00 Idle, 01 Transmit, 10 Clock Toggle, 11 Error
    cs_b = 1
    spi_clk = 0
    spi_data = 0
    bits_left = 16
    done = 0
    shift_reg = 0

    result = []
    prev_clk = None
    auto_pos = True

    for row in vectors:
        rst_b = int(row.get('i_rst_b', 1)) & 1

        if rst_b == 0:
            state = 0
            cs_b = 1
            spi_clk = 0
            spi_data = 0
            bits_left = 16
            done = 0
            shift_reg = 0

        edge = None

        e = row.get('edge', None)
        if e is None:
            e = row.get('i_clk_edge', row.get('clk_edge', None))

        if e is not None:
            if isinstance(e, str):
                s = e.lower()
                if ('pos' in s) or ('rise' in s) or ('up' in s):
                    edge = 1
                elif ('neg' in s) or ('fall' in s) or ('down' in s):
                    edge = 0
            else:
                edge = 1 if int(e) != 0 else 0

        clk_val = row.get('i_clk', row.get('clk', None))

        if edge is None:
            if clk_val is not None:
                cv = int(clk_val) & 1
                if prev_clk is not None and cv != prev_clk:
                    edge = 1 if cv == 1 else 0
                else:
                    edge = 1 if cv == 1 else 0
            else:
                edge = 1 if auto_pos else 0
                auto_pos = not auto_pos

        if clk_val is not None:
            prev_clk = int(clk_val) & 1

        result.append({
            'o_spi_cs_b': int(cs_b) & 1,
            'o_spi_clk': int(spi_clk) & 1,
            'o_spi_data': int(spi_data) & 1,
            'o_bits_left': int(bits_left) & 0x1F,
            'o_done': int(done) & 1,
            'o_fsm_state': int(state) & 0x3
        })

        if edge == 1 and rst_b == 1:
            clear = int(row.get('i_clear', 0)) & 1
            fault = int(row.get('i_fault', 0)) & 1
            enable = int(row.get('i_enable', 0)) & 1
            data_in = int(row.get('i_data_in', 0)) & 0xFFFF

            if clear:
                state = 0
                cs_b = 1
                spi_clk = 0
                spi_data = 0
                bits_left = 16
                done = 0
                shift_reg = 0

            elif fault:
                if state != 3:
                    state = 3
                    cs_b = 1
                    spi_clk = 0
                    spi_data = 0
                    bits_left = 16
                    done = 1
                else:
                    state = 3
                    cs_b = 1
                    spi_clk = 0
                    spi_data = 0
                    bits_left = 16
                    done = 0

            elif state == 3:
                state = 3
                cs_b = 1
                spi_clk = 0
                spi_data = 0
                bits_left = 16
                done = 0

            elif enable == 0:
                state = 0
                cs_b = 1
                spi_clk = 0
                spi_data = 0
                bits_left = 16
                done = 0

            else:
                if state == 0:
                    cs_b = 1
                    spi_clk = 0
                    spi_data = 0
                    bits_left = 16
                    done = 0
                    state = 1
                    shift_reg = data_in

                elif state == 1:
                    done = 0
                    cs_b = 0
                    spi_data = (shift_reg >> 15) & 1
                    shift_reg = (shift_reg << 1) & 0xFFFF
                    state = 2

                elif state == 2:
                    if bits_left == 1:
                        cs_b = 1
                        spi_clk = 0
                        bits_left = 0
                        done = 1
                        state = 0
                    else:
                        spi_clk = spi_clk ^ 1
                        bits_left = (bits_left - 1) & 0x1F
                        done = 0
                        state = 1

    return result
