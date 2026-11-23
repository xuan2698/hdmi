def reference(vectors):
    enc_data = 0
    enc_valid = 0
    dec_data = 0
    dec_valid = 0
    prev_clk = 0
    N = 8
    res = []
    for idx, row in enumerate(vectors):
        if isinstance(row, dict):
            rst = row.get('rst_in', 0)
            enc_v_in = row.get('enc_valid_in', 0)
            enc_d_in = row.get('enc_data_in', 0)
            dec_v_in = row.get('dec_valid_in', 0)
            dec_d_in = row.get('dec_data_in', 0)
        else:
            rst = row[0] if len(row) > 0 else 0
            enc_v_in = row[1] if len(row) > 1 else 0
            enc_d_in = row[2] if len(row) > 2 else 0
            dec_v_in = row[3] if len(row) > 3 else 0
            dec_d_in = row[4] if len(row) > 4 else 0

        edge = None
        if isinstance(row, dict):
            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    edge = 'pos' if 'pos' in e.lower() else ('neg' if 'neg' in e.lower() else None)
                else:
                    edge = 'pos' if e == 1 else 'neg'
            elif 'clk_in' in row:
                clk = row['clk_in']
                if prev_clk == 0 and clk == 1:
                    edge = 'pos'
                elif prev_clk == 1 and clk == 0:
                    edge = 'neg'
                prev_clk = clk
        if edge is None:
            edge = 'pos' if idx % 2 == 0 else 'neg'

        if rst == 1:
            enc_data = 0
            enc_valid = 0
            dec_data = 0
            dec_valid = 0

        res.append({
            'enc_valid_out': enc_valid & 1,
            'enc_data_out': enc_data & 0xFFFF,
            'dec_valid_out': dec_valid & 1,
            'dec_data_out': dec_data & 0xFF
        })

        if edge == 'pos' and rst == 0:
            e_val = 0
            for i in range(N):
                if (enc_d_in >> i) & 1:
                    e_val |= (1 << (2 * i))
                else:
                    e_val |= (2 << (2 * i))
            enc_data = e_val & 0xFFFF
            enc_valid = enc_v_in & 1

            d_val = 0
            for i in range(N):
                pair = (dec_d_in >> (2 * i)) & 3
                if pair == 1:
                    d_val |= (1 << i)
            dec_data = d_val & 0xFF
            dec_valid = dec_v_in & 1
    return res
