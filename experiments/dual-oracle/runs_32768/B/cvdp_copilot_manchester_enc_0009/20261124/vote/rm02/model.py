def reference(vectors):
    enc_data_out = 0
    enc_valid_out = 0
    dec_data_out = 0
    dec_valid_out = 0
    result = []
    for idx, row in enumerate(vectors):
        rst = row.get('rst_in', 0) & 1
        if rst:
            enc_data_out = 0
            enc_valid_out = 0
            dec_data_out = 0
            dec_valid_out = 0

        if 'clk_in' in row:
            posedge = (row.get('clk_in', 0) & 1) == 1
        else:
            posedge = (idx % 2) == 0

        result.append({
            'enc_valid_out': enc_valid_out & 1,
            'enc_data_out': enc_data_out & 0xFFFF,
            'dec_valid_out': dec_valid_out & 1,
            'dec_data_out': dec_data_out & 0xFF,
        })

        if posedge:
            if rst:
                enc_data_out = 0
                enc_valid_out = 0
                dec_data_out = 0
                dec_valid_out = 0
            else:
                enc_in = row.get('enc_data_in', 0) & 0xFF
                new_enc = 0
                for i in range(8):
                    bit = (enc_in >> i) & 1
                    pair = 1 if bit else 2
                    new_enc |= pair << (2 * i)
                enc_data_out = new_enc & 0xFFFF
                enc_valid_out = row.get('enc_valid_in', 0) & 1

                dec_in = row.get('dec_data_in', 0) & 0xFFFF
                new_dec = 0
                for i in range(8):
                    pair = (dec_in >> (2 * i)) & 3
                    if pair == 1:
                        new_dec |= 1 << i
                dec_data_out = new_dec & 0xFF
                dec_valid_out = row.get('dec_valid_in', 0) & 1

    return result
