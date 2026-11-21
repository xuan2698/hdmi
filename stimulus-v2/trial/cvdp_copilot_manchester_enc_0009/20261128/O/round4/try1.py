def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        rst = 1 if i < 3 else 0
        enc_valid = 0
        enc_data = 0
        dec_valid = 0
        dec_data = 0
        if rst == 0:
            if i < 10:
                enc_valid = 1
                enc_data = rng.randrange(256)
                dec_valid = 1
                dec_data = rng.randrange(65536)
            elif i < 22:
                enc_valid = 1
                enc_data = rng.randrange(256)
                dec_valid = 0
                dec_data = 0
            elif i < 34:
                enc_valid = 0
                enc_data = 0
                dec_valid = 1
                dec_data = rng.randrange(65536)
            elif i < 40:
                enc_valid = 0
                enc_data = 0
                dec_valid = 0
                dec_data = 0
            else:
                r = rng.random()
                if r < 0.4:
                    enc_valid = 1
                    enc_data = rng.randrange(256)
                elif r < 0.8:
                    dec_valid = 1
                    dec_data = rng.randrange(65536)
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
        rows.append(row)
    return rows
