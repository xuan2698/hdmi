def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        rst = 1 if i < 3 else 0
        enc_valid = 0
        enc_data = 0
        dec_valid = 0
        dec_data = 0
        if rst == 0:
            phase = (i - 3) % 24
            if phase < 3:
                enc_valid = 1
                enc_data = rng.randrange(256)
            elif phase < 6:
                dec_valid = 1
                dec_data = rng.randrange(65536)
            elif phase < 8:
                enc_valid = 1
                enc_data = rng.randrange(256)
                dec_valid = 1
                dec_data = rng.randrange(65536)
            elif phase == 8:
                enc_valid = 1
                enc_data = 0
            elif phase == 9:
                enc_valid = 1
                enc_data = 255
            elif phase == 10:
                dec_valid = 1
                dec_data = 0xAAAA
            elif phase == 11:
                dec_valid = 1
                dec_data = 0x5555
            elif phase == 12:
                dec_valid = 1
                dec_data = 0xFFFF
            elif phase == 13:
                dec_valid = 1
                dec_data = 0x0000
            elif phase == 14:
                enc_valid = 1
                enc_data = 0x0F
                dec_valid = 1
                dec_data = 0x0F0F
            elif phase == 15:
                enc_valid = 1
                enc_data = 0xF0
                dec_valid = 1
                dec_data = 0xF0F0
            elif phase == 16:
                enc_valid = 1
                enc_data = 0xAA
            elif phase == 17:
                dec_valid = 1
                dec_data = 0x3333
            elif phase == 18:
                enc_valid = 1
                enc_data = 0x55
                dec_valid = 1
                dec_data = 0xCCCC
            elif phase == 19:
                enc_valid = 1
                enc_data = rng.randrange(256)
            elif phase == 20:
                dec_valid = 1
                dec_data = rng.randrange(65536)
            elif phase == 21:
                enc_valid = 1
                enc_data = rng.randrange(256)
                dec_valid = 1
                dec_data = rng.randrange(65536)
            elif phase == 22:
                enc_valid = 1
                enc_data = 0x81
            else:
                dec_valid = 1
                dec_data = 0x8181
        row = {
            'rst_in': rst,
            'enc_valid_in': enc_valid,
            'enc_data_in': enc_data,
            'dec_valid_in': dec_valid,
            'dec_data_in': dec_data,
        }
        if rst == 0 and rng.random() < 0.10:
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
