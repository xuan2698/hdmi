def stimulus(rng, cycles):
    rows = []
    rst_remaining = 3
    enc_run = 0
    dec_run = 0
    enc_data = 0
    dec_data = 0
    enc_pattern = 0
    dec_pattern = 0
    for i in range(cycles):
        rst = 1 if rst_remaining > 0 else 0
        if rst_remaining > 0:
            rst_remaining -= 1
        enc_valid = 0
        dec_valid = 0
        if rst == 0:
            if enc_run > 0:
                enc_valid = 1
                enc_run -= 1
            elif rng.random() < 0.45:
                enc_valid = 1
                enc_pattern = rng.randrange(4)
                if enc_pattern == 0:
                    enc_data = 0
                elif enc_pattern == 1:
                    enc_data = 255
                elif enc_pattern == 2:
                    enc_data = rng.randrange(256)
                else:
                    enc_data = (1 << rng.randrange(8))
                enc_run = rng.randrange(1, 10)
            if dec_run > 0:
                dec_valid = 1
                dec_run -= 1
            elif rng.random() < 0.45:
                dec_valid = 1
                dec_pattern = rng.randrange(5)
                if dec_pattern == 0:
                    dec_data = 0
                elif dec_pattern == 1:
                    dec_data = 65535
                elif dec_pattern == 2:
                    dec_data = 0xAAAA
                elif dec_pattern == 3:
                    dec_data = 0x5555
                else:
                    dec_data = rng.randrange(65536)
                dec_run = rng.randrange(1, 10)
        row = {
            'rst_in': rst,
            'enc_valid_in': enc_valid,
            'enc_data_in': enc_data if enc_valid else 0,
            'dec_valid_in': dec_valid,
            'dec_data_in': dec_data if dec_valid else 0,
        }
        if rst == 0 and rng.random() < 0.04:
            row['mid'] = {'rst_in': 1, 'enc_valid_in': 0, 'enc_data_in': 0,
                          'dec_valid_in': 0, 'dec_data_in': 0}
        rows.append(row)
    return rows
