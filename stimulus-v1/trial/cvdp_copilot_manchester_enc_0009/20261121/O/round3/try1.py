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
                    enc_data = 0xFF if (i & 1) else 0x00
                elif enc_mode == 3:
                    enc_data = (enc_data << 1) & 0xFF
            elif rng.random() < 0.45:
                enc_valid = 1
                enc_mode = rng.randrange(4)
                if enc_mode == 0:
                    enc_data = rng.randrange(256)
                elif enc_mode == 1:
                    enc_data = rng.randrange(256)
                elif enc_mode == 2:
                    enc_data = 0xAA if rng.random() < 0.5 else 0x55
                else:
                    enc_data = 1 << rng.randrange(8)
                enc_run = rng.randrange(1, 10)
            if dec_run > 0:
                dec_valid = 1
                dec_run -= 1
                if dec_mode == 1:
                    dec_data = (dec_data + 0x0101) & 0xFFFF
                elif dec_mode == 2:
                    dec_data = 0xAAAA if (i & 1) else 0x5555
                elif dec_mode == 3:
                    dec_data = (dec_data << 2) & 0xFFFF
            elif rng.random() < 0.45:
                dec_valid = 1
                dec_mode = rng.randrange(4)
                if dec_mode == 0:
                    dec_data = rng.randrange(65536)
                elif dec_mode == 1:
                    dec_data = rng.randrange(65536)
                elif dec_mode == 2:
                    dec_data = 0xAAAA if rng.random() < 0.5 else 0x5555
                else:
                    dec_data = (rng.randrange(256) << 8) | rng.randrange(256)
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
