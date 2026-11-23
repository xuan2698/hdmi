def reference(vectors):
    N = 8
    enc_valid_out = 0
    enc_data_out = 0
    dec_valid_out = 0
    dec_data_out = 0
    outputs = []
    for idx, row in enumerate(vectors):
        rst = row.get('rst_in', 0)
        if rst:
            enc_valid_out = 0
            enc_data_out = 0
            dec_valid_out = 0
            dec_data_out = 0
        outputs.append({
            'enc_valid_out': enc_valid_out,
            'enc_data_out': enc_data_out,
            'dec_valid_out': dec_valid_out,
            'dec_data_out': dec_data_out
        })
        if idx % 2 == 0 and not rst:
            enc_valid_in = row.get('enc_valid_in', 0)
            enc_data_in = row.get('enc_data_in', 0)
            dec_valid_in = row.get('dec_valid_in', 0)
            dec_data_in = row.get('dec_data_in', 0)
            next_enc_data = 0
            for i in range(N):
                d = (enc_data_in >> i) & 1
                next_enc_data |= (d << (2 * i)) | ((1 - d) << (2 * i + 1))
            next_dec_data = 0
            for i in range(N):
                low = (dec_data_in >> (2 * i)) & 1
                high = (dec_data_in >> (2 * i + 1)) & 1
                bit = low if high != low else 0
                next_dec_data |= bit << i
            enc_valid_out = enc_valid_in
            enc_data_out = next_enc_data
            dec_valid_out = dec_valid_in
            dec_data_out = next_dec_data
    return outputs
