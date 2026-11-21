def stimulus(rng, cycles):
    rows = []
    rst_remaining = 4
    enc_run = 0
    dec_run = 0
    enc_data = 0
    dec_data = 0
    enc_mode = 0
    dec_mode = 0
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
                if enc_mode == 1:
                    enc_data = (enc_data + 1) & 0xFF
                elif enc_mode == 2:
                    enc_data = rng.randrange(256)
            else:
                r = rng.random()
                if r < 0.35:
                    enc_valid = 1
                    enc_mode = rng.randrange(3)
                    if enc_mode == 0:
                        enc_data = rng.choice([0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x81, 0x7E])
                    elif enc_mode == 1:
                        enc_data = rng.randrange(256)
                    else:
                        enc_data = rng.randrange(256)
                    enc_run = rng.randrange(1, 10)
            if dec_run > 0:
                dec_valid = 1
                dec_run -= 1
                if dec_mode == 1:
                    dec_data = (dec_data + 0x0101) & 0xFFFF
                elif dec_mode == 2:
                    dec_data = rng.randrange(65536)
            else:
                r = rng.random()
                if r < 0.35:
                    dec_valid = 1
                    dec_mode = rng.randrange(3)
                    if dec_mode == 0:
                        dec_data = rng.choice([0x0000, 0xFFFF, 0xAAAA, 0x5555, 0x00FF, 0xFF00, 0x8001, 0x7FFE])
                    elif dec_mode == 1:
                        dec_data = rng.randrange(65536)
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
        rows.append(row)
    return rows
