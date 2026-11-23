def reference(vectors):
    N = 8
    enc_data_out = 0
    enc_valid_out = 0
    dec_data_out = 0
    dec_valid_out = 0
    prev_clk = 0
    results = []
    for idx, row in enumerate(vectors):
        rst = row.get('rst_in', 0) & 1
        enc_valid_in = row.get('enc_valid_in', 0) & 1
        enc_data_in = row.get('enc_data_in', 0) & 0xFF
        dec_valid_in = row.get('dec_valid_in', 0) & 1
        dec_data_in = row.get('dec_data_in', 0) & 0xFFFF

        if rst:
            enc_data_out = 0
            enc_valid_out = 0
            dec_data_out = 0
            dec_valid_out = 0

        is_posedge = False
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                is_posedge = ('pos' in e.lower()) or (e == '1')
            else:
                is_posedge = bool(e)
        else:
            clk = None
            for k in ('clk_in', 'clk', 'clock'):
                if k in row:
                    clk = row[k]
                    break
            if clk is not None:
                clk_val = clk & 1
                is_posedge = (clk_val == 1 and prev_clk == 0)
                prev_clk = clk_val
            else:
                is_posedge = (idx % 2 == 0)

        results.append({
            'enc_valid_out': int(enc_valid_out),
            'enc_data_out': int(enc_data_out),
            'dec_valid_out': int(dec_valid_out),
            'dec_data_out': int(dec_data_out)
        })

        if is_posedge:
            if rst:
                enc_data_out = 0
                enc_valid_out = 0
                dec_data_out = 0
                dec_valid_out = 0
            else:
                encoded = 0
                for i in range(N):
                    bit = (enc_data_in >> i) & 1
                    pair = 1 if bit else 2
                    encoded |= (pair << (2 * i))
                enc_data_out = encoded & 0xFFFF
                enc_valid_out = enc_valid_in

                decoded = 0
                for i in range(N):
                    pair = (dec_data_in >> (2 * i)) & 3
                    if pair == 1:
                        decoded |= (1 << i)
                dec_data_out = decoded & 0xFF
                dec_valid_out = dec_valid_in

    return results
