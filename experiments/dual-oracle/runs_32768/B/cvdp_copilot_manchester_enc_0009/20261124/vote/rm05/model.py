def reference(vectors):
    N = 8
    state = [0, 0, 0, 0]
    result = []
    for idx, row in enumerate(vectors):
        if row.get('rst_in', 0):
            state = [0, 0, 0, 0]
        if 'clk_in' in row:
            posedge = bool(row.get('clk_in'))
        elif 'edge' in row:
            e = row.get('edge')
            posedge = (e == 1 or e is True or (isinstance(e, str) and 'pos' in e.lower()))
        else:
            posedge = (idx % 2 == 0)
        ev, ed, dv, dd = state
        result.append({
            'enc_valid_out': ev & 1,
            'enc_data_out': ed & 0xFFFF,
            'dec_valid_out': dv & 1,
            'dec_data_out': dd & 0xFF
        })
        if posedge:
            if row.get('rst_in', 0):
                state = [0, 0, 0, 0]
            else:
                enc_v = row.get('enc_valid_in', 0) & 1
                dec_v = row.get('dec_valid_in', 0) & 1
                new_ev = enc_v
                new_dv = dec_v
                new_ed = state[1]
                new_dd = state[3]
                if enc_v:
                    data = row.get('enc_data_in', 0) & 0xFF
                    val = 0
                    for i in range(N):
                        if (data >> i) & 1:
                            val |= 1 << (2 * i)
                        else:
                            val |= 2 << (2 * i)
                    new_ed = val & 0xFFFF
                if dec_v:
                    data = row.get('dec_data_in', 0) & 0xFFFF
                    val = 0
                    for i in range(N):
                        if ((data >> (2 * i)) & 3) == 1:
                            val |= 1 << i
                    new_dd = val & 0xFF
                state = [new_ev, new_ed, new_dv, new_dd]
    return result
