def stimulus(rng, cycles):
    rows = []
    rst_in = 1
    enc_valid_in = 0
    enc_data_in = 0
    dec_valid_in = 0
    dec_data_in = 0
    for c in range(cycles):
        if c < 3:
            rst_in = 1
            enc_valid_in = 0
            enc_data_in = 0
            dec_valid_in = 0
            dec_data_in = 0
        elif c == 3:
            rst_in = 0
            enc_valid_in = 0
            enc_data_in = 0
            dec_valid_in = 0
            dec_data_in = 0
        elif c < 8:
            rst_in = 0
            enc_valid_in = 1
            enc_data_in = (enc_data_in + 0x5A) & 0xFF
            dec_valid_in = 1
            dec_data_in = (dec_data_in + 0xA5A5) & 0xFFFF
        else:
            rst_in = 0
            r = rng.random()
            if r < 0.45:
                enc_valid_in = 1
                enc_data_in = rng.randrange(256)
            elif r < 0.60:
                enc_valid_in = 0
                enc_data_in = 0
            else:
                enc_valid_in = rng.randrange(2)
                enc_data_in = rng.randrange(256) if enc_valid_in else 0
            r2 = rng.random()
            if r2 < 0.45:
                dec_valid_in = 1
                dec_data_in = rng.randrange(65536)
            elif r2 < 0.60:
                dec_valid_in = 0
                dec_data_in = 0
            else:
                dec_valid_in = rng.randrange(2)
                dec_data_in = rng.randrange(65536) if dec_valid_in else 0
        row = {
            'rst_in': rst_in,
            'enc_valid_in': enc_valid_in,
            'enc_data_in': enc_data_in,
            'dec_valid_in': dec_valid_in,
            'dec_data_in': dec_data_in,
        }
        rows.append(row)
    return rows
