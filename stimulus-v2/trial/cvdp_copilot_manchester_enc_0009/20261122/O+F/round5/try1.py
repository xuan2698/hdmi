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
        elif c < 5:
            rst = 0
            enc_v = 0
            enc_d = 0
            dec_v = 0
            dec_d = 0
        else:
            rst = 0
            if rng.random() < 0.45:
                enc_v = 1
                enc_d = rng.randrange(256)
            else:
                enc_v = 0
                enc_d = 0
            if rng.random() < 0.45:
                dec_v = 1
                if rng.random() < 0.5:
                    dec_d = rng.randrange(65536)
                else:
                    v = 0
                    for i in range(8):
                        b = rng.randrange(4)
                        if b == 0:
                            v |= (1 << (2 * i))
                        elif b == 1:
                            v |= (1 << (2 * i + 1))
                    dec_d = v
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
        if c >= 5 and rng.random() < 0.25:
            mid = {}
            if rng.random() < 0.5:
                mid['enc_valid_in'] = rng.randrange(2)
                mid['enc_data_in'] = rng.randrange(256)
            if rng.random() < 0.5:
                mid['dec_valid_in'] = rng.randrange(2)
                mid['dec_data_in'] = rng.randrange(65536)
            if rng.random() < 0.08:
                mid['rst_in'] = 1
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows
