def stimulus(rng, cycles):
    rows = []
    rst = 1
    enc_v = 0
    enc_d = 0
    dec_v = 0
    dec_d = 0
    for c in range(cycles):
        if c < 2:
            rst = 1
            enc_v = 0
            enc_d = 0
            dec_v = 0
            dec_d = 0
        elif c == 2:
            rst = 0
            enc_v = 0
            enc_d = 0
            dec_v = 0
            dec_d = 0
        else:
            rst = 0
            r = rng.random()
            if r < 0.40:
                enc_v = 1
                enc_d = rng.randrange(256)
            else:
                enc_v = 0
                enc_d = 0
            r2 = rng.random()
            if r2 < 0.40:
                dec_v = 1
                dec_d = rng.randrange(65536)
            else:
                dec_v = 0
                dec_d = 0
        row = {
            'rst_in': rst,
            'enc_valid_in': enc_v,
            'enc_data_in': enc_d,
            'dec_valid_in': dec_v,
            'dec_data_in': dec_d,
        }
        if c == 1:
            row['mid'] = {'rst_in': 1, 'enc_valid_in': 0, 'enc_data_in': 0, 'dec_valid_in': 0, 'dec_data_in': 0}
        elif c == 2:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 1, 'enc_data_in': 22, 'dec_valid_in': 1, 'dec_data_in': 0}
        rows.append(row)
    return rows
