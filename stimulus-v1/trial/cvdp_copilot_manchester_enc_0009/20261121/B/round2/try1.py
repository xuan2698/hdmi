def stimulus(rng, cycles):
    rows = []
    rst_remaining = 3
    enc_run = 0
    dec_run = 0
    enc_data = 0
    dec_data = 0
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
            elif rng.random() < 0.35:
                enc_valid = 1
                enc_data = rng.randrange(256)
                enc_run = rng.randrange(1, 6)
            if dec_run > 0:
                dec_valid = 1
                dec_run -= 1
            elif rng.random() < 0.35:
                dec_valid = 1
                dec_data = rng.randrange(65536)
                dec_run = rng.randrange(1, 6)
        row = {
            'rst_in': rst,
            'enc_valid_in': enc_valid,
            'enc_data_in': enc_data if enc_valid else 0,
            'dec_valid_in': dec_valid,
            'dec_data_in': dec_data if dec_valid else 0,
        }
        rows.append(row)
    return rows
