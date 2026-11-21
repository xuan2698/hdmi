def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        rst = 1 if i < 3 else 0
        enc_valid = 0
        enc_data = 0
        dec_valid = 0
        dec_data = 0
        if rst == 0:
            phase = i % 16
            if phase < 4:
                enc_valid = 1
                enc_data = rng.randrange(256)
            elif phase < 8:
                dec_valid = 1
                dec_data = rng.randrange(65536)
            elif phase < 10:
                enc_valid = 1
                enc_data = rng.randrange(256)
                dec_valid = 1
                dec_data = rng.randrange(65536)
            elif phase == 10:
                enc_valid = 1
                enc_data = 0
            elif phase == 11:
                enc_valid = 1
                enc_data = 255
            elif phase == 12:
                dec_valid = 1
                dec_data = 0xAAAA
            elif phase == 13:
                dec_valid = 1
                dec_data = 0x5555
            elif phase == 14:
                dec_valid = 1
                dec_data = 0xFFFF
            else:
                enc_valid = 1
                enc_data = rng.randrange(256)
                dec_valid = 1
                dec_data = rng.randrange(65536)
        row = {
            'rst_in': rst,
            'enc_valid_in': enc_valid,
            'enc_data_in': enc_data,
            'dec_valid_in': dec_valid,
            'dec_data_in': dec_data,
        }
        if rst == 0 and rng.random() < 0.12:
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
