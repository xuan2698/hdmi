def stimulus(rng, cycles):
    rows = []
    rst_high = 4
    enc_patterns = [0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x81, 0x18, 0x3C, 0xC3]
    dec_patterns = [0x0000, 0xFFFF, 0xAAAA, 0x5555, 0x00FF, 0xFF00, 0x8001, 0x0180, 0x3CC3, 0xC33C]
    for i in range(cycles):
        row = {
            'rst_in': 1 if i < rst_high else 0,
            'enc_valid_in': 0,
            'enc_data_in': 0,
            'dec_valid_in': 0,
            'dec_data_in': 0,
        }
        if i >= rst_high:
            mode = rng.randrange(100)
            if mode < 25:
                row['enc_valid_in'] = 1
                if rng.randrange(3) == 0:
                    row['enc_data_in'] = enc_patterns[rng.randrange(len(enc_patterns))]
                else:
                    row['enc_data_in'] = rng.randrange(256)
            elif mode < 50:
                row['dec_valid_in'] = 1
                if rng.randrange(3) == 0:
                    row['dec_data_in'] = dec_patterns[rng.randrange(len(dec_patterns))]
                else:
                    row['dec_data_in'] = rng.randrange(65536)
            elif mode < 70:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif mode < 80:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0
            elif mode < 90:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xFFFF
            else:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xFF
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xAAAA
        rows.append(row)
    return rows
