def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        rst = 1 if i < 3 else 0
        enc_valid = 0
        enc_data = 0
        dec_valid = 0
        dec_data = 0
        if rst == 0:
            phase = (i - 3) % 32
            if phase < 4:
                enc_valid = 1
                enc_data = rng.randrange(256)
            elif phase < 8:
                dec_valid = 1
                dec_data = rng.randrange(65536)
            elif phase < 12:
                enc_valid = 1
                enc_data = rng.randrange(256)
                dec_valid = 1
                dec_data = rng.randrange(65536)
            elif phase == 12:
                enc_valid = 1
                enc_data = 0x00
            elif phase == 13:
                enc_valid = 1
                enc_data = 0xFF
            elif phase == 14:
                enc_valid = 1
                enc_data = 0xAA
            elif phase == 15:
                enc_valid = 1
                enc_data = 0x55
            elif phase == 16:
                dec_valid = 1
                dec_data = 0xAAAA
            elif phase == 17:
                dec_valid = 1
                dec_data = 0x5555
            elif phase == 18:
                dec_valid = 1
                dec_data = 0xFFFF
            elif phase == 19:
                dec_valid = 1
                dec_data = 0x0000
            elif phase == 20:
                dec_valid = 1
                dec_data = 0xCCCC
            elif phase == 21:
                dec_valid = 1
                dec_data = 0x3333
            elif phase == 22:
                enc_valid = 1
                enc_data = 0xAA
                dec_valid = 1
                dec_data = 0xCCCC
            elif phase == 23:
                enc_valid = 1
                enc_data = 0x55
                dec_valid = 1
                dec_data = 0x3333
            elif phase == 24:
                enc_valid = 1
                enc_data = rng.randrange(256)
            elif phase == 25:
                dec_valid = 1
                dec_data = rng.randrange(65536)
            elif phase == 26:
                enc_valid = 1
                enc_data = 0x0F
                dec_valid = 1
                dec_data = 0x0F0F
            elif phase == 27:
                enc_valid = 1
                enc_data = 0xF0
                dec_valid = 1
                dec_data = 0xF0F0
            elif phase == 28:
                enc_valid = 1
                enc_data = 0x81
            elif phase == 29:
                dec_valid = 1
                dec_data = 0x8001
            elif phase == 30:
                enc_valid = 1
                enc_data = rng.randrange(256)
                dec_valid = 1
                dec_data = rng.randrange(65536)
            else:
                enc_valid = 0
                dec_valid = 0
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
