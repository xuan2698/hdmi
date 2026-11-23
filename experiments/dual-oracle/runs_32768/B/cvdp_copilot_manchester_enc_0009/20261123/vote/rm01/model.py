def reference(vectors):
    enc_data_reg = 0
    enc_valid_reg = 0
    dec_data_reg = 0
    dec_valid_reg = 0
    results = []
    N = 8
    for i, row in enumerate(vectors):
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                is_posedge = 'pos' in e.lower()
            else:
                is_posedge = bool(e)
        elif 'clk_in' in row:
            is_posedge = bool(row['clk_in'])
        else:
            is_posedge = (i % 2 == 0)

        rst = row.get('rst_in', 0)
        if rst:
            enc_data_reg = 0
            enc_valid_reg = 0
            dec_data_reg = 0
            dec_valid_reg = 0

        results.append({
            'enc_valid_out': enc_valid_reg,
            'enc_data_out': enc_data_reg,
            'dec_valid_out': dec_valid_reg,
            'dec_data_out': dec_data_reg
        })

        if is_posedge and not rst:
            enc_valid_in = row.get('enc_valid_in', 0)
            enc_data_in = row.get('enc_data_in', 0)
            dec_valid_in = row.get('dec_valid_in', 0)
            dec_data_in = row.get('dec_data_in', 0)

            enc_new = 0
            for j in range(N):
                b = (enc_data_in >> j) & 1
                if b:
                    enc_new |= (1 << (2 * j))
                else:
                    enc_new |= (2 << (2 * j))
            enc_data_reg = enc_new
            enc_valid_reg = enc_valid_in

            dec_new = 0
            for j in range(N):
                pair = (dec_data_in >> (2 * j)) & 3
                if pair == 1:
                    dec_new |= (1 << j)
            dec_data_reg = dec_new
            dec_valid_reg = dec_valid_in

    return results
