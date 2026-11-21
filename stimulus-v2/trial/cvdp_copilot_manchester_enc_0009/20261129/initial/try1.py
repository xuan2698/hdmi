def stimulus(rng, cycles):
    rows = []
    rst = 1
    enc_valid = 0
    enc_data = 0
    dec_valid = 0
    dec_data = 0
    for i in range(cycles):
        if i < 3:
            rst = 1
        elif i < 5:
            rst = 0
        else:
            rst = 0
        if i >= 5:
            r = rng.random()
            if r < 0.35:
                enc_valid = 1
                enc_data = rng.randrange(256)
            elif r < 0.55:
                enc_valid = 0
                enc_data = 0
            else:
                enc_valid = 0
                enc_data = 0
            r2 = rng.random()
            if r2 < 0.35:
                dec_valid = 1
                dec_data = rng.randrange(65536)
            else:
                dec_valid = 0
                dec_data = 0
        else:
            enc_valid = 0
            enc_data = 0
            dec_valid = 0
            dec_data = 0
        row = {
            'rst_in': rst,
            'enc_valid_in': enc_valid,
            'enc_data_in': enc_data,
            'dec_valid_in': dec_valid,
            'dec_data_in': dec_data,
        }
        rows.append(row)
    return rows
