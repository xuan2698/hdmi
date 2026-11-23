def reference(vectors):
    enc_valid_out = 0
    enc_data_out = 0
    dec_valid_out = 0
    dec_data_out = 0
    result = []
    posedge = True
    for row in vectors:
        rst = row.get('rst_in', 0) & 1
        if rst:
            enc_valid_out = 0
            enc_data_out = 0
            dec_valid_out = 0
            dec_data_out = 0
        result.append({
            'enc_valid_out': enc_valid_out,
            'enc_data_out': enc_data_out,
            'dec_valid_out': dec_valid_out,
            'dec_data_out': dec_data_out
        })
        if posedge and not rst:
            enc_valid_in = row.get('enc_valid_in', 0) & 1
            enc_data_in = row.get('enc_data_in', 0) & 0xFF
            dec_valid_in = row.get('dec_valid_in', 0) & 1
            dec_data_in = row.get('dec_data_in', 0) & 0xFFFF

            encoded = 0
            for i in range(8):
                bit = (enc_data_in >> i) & 1
                pair = 1 if bit else 2
                encoded |= pair << (2 * i)
            enc_data_out = encoded & 0xFFFF

            decoded = 0
            for i in range(8):
                pair = (dec_data_in >> (2 * i)) & 3
                if pair == 1:
                    decoded |= 1 << i
            dec_data_out = decoded & 0xFF

            enc_valid_out = enc_valid_in
            dec_valid_out = dec_valid_in
        posedge = not posedge
    return result
