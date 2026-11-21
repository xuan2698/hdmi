def stimulus(rng, cycles):
    rows = []
    rst_high = 3
    for i in range(cycles):
        rst = 1 if i < rst_high else 0
        enc_valid = 0
        enc_data = 0
        dec_valid = 0
        dec_data = 0
        if rst == 0:
            r = rng.random()
            if r < 0.35:
                enc_valid = 1
                enc_data = rng.randrange(256)
            elif r < 0.55:
                dec_valid = 1
                dec_data = rng.randrange(65536)
            elif r < 0.70:
                enc_valid = 1
                enc_data = rng.randrange(256)
                dec_valid = 1
                dec_data = rng.randrange(65536)
            elif r < 0.80:
                enc_valid = 1
                enc_data = 0
            elif r < 0.88:
                enc_valid = 1
                enc_data = 255
            elif r < 0.94:
                dec_valid = 1
                dec_data = 0xAAAA
            else:
                dec_valid = 1
                dec_data = 0x5555
        row = {
            'rst_in': rst,
            'enc_valid_in': enc_valid,
            'enc_data_in': enc_data,
            'dec_valid_in': dec_valid,
            'dec_data_in': dec_data,
        }
        if rst == 0 and rng.random() < 0.15:
            mid = {}
            if rng.random() < 0.5:
                mid['enc_valid_in'] = rng.randrange(2)
                mid['enc_data_in'] = rng.randrange(256)
            else:
                mid['dec_valid_in'] = rng.randrange(2)
                mid['dec_data_in'] = rng.randrange(65536)
            row['mid'] = mid
        rows.append(row)
    return rows
