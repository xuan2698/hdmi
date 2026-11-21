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
            enc_v = 0
            enc_d = 0
            dec_v = 0
            dec_d = 0
        else:
            rst = 0
            if c < 6:
                enc_v = 0
                enc_d = 0
                dec_v = 0
                dec_d = 0
            else:
                r = rng.random()
                if r < 0.45:
                    enc_v = 1
                    enc_d = rng.randrange(256)
                else:
                    enc_v = 0
                    enc_d = 0
                r2 = rng.random()
                if r2 < 0.45:
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
        if c >= 6 and rng.random() < 0.18:
            mid = {}
            if rng.random() < 0.5:
                mid['enc_valid_in'] = rng.randrange(2)
                mid['enc_data_in'] = rng.randrange(256)
            if rng.random() < 0.5:
                mid['dec_valid_in'] = rng.randrange(2)
                mid['dec_data_in'] = rng.randrange(65536)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows
