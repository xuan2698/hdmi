def stimulus(rng, cycles):
    rows = []
    rst = 1
    enc_v = 0
    enc_d = 0
    dec_v = 0
    dec_d = 0
    for c in range(cycles):
        if c < 3:
            rst = 1
        else:
            rst = 0
        if c >= 3:
            r = rng.random()
            if r < 0.35:
                enc_v = 1
                enc_d = rng.randrange(256)
            elif r < 0.55:
                enc_v = 0
                enc_d = 0
            else:
                enc_v = 0
                enc_d = 0
            r2 = rng.random()
            if r2 < 0.35:
                dec_v = 1
                dec_d = rng.randrange(65536)
            else:
                dec_v = 0
                dec_d = 0
        else:
            enc_v = 0
            enc_d = 0
            dec_v = 0
            dec_d = 0
        row = {
            'rst_in': rst,
            'enc_valid_in': enc_v,
            'enc_data_in': enc_d,
            'dec_valid_in': dec_v,
            'dec_data_in': dec_d,
        }
        if c % 7 == 3 and c >= 3:
            row['mid'] = {
                'enc_valid_in': rng.randrange(2),
                'enc_data_in': rng.randrange(256),
                'dec_valid_in': rng.randrange(2),
                'dec_data_in': rng.randrange(65536),
            }
        rows.append(row)
    return rows
