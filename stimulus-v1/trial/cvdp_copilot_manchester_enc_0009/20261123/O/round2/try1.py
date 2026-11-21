def stimulus(rng, cycles):
    rows = []
    rst_high = 3
    enc_patterns = [0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x81, 0x7E]
    dec_patterns = [0x0000, 0xFFFF, 0xAAAA, 0x5555, 0x00FF, 0xFF00, 0x8001, 0x7FFE]
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
            if mode < 35:
                row['enc_valid_in'] = 1
                if rng.randrange(100) < 50:
                    row['enc_data_in'] = enc_patterns[rng.randrange(len(enc_patterns))]
                else:
                    row['enc_data_in'] = rng.randrange(256)
            elif mode < 70:
                row['dec_valid_in'] = 1
                if rng.randrange(100) < 50:
                    row['dec_data_in'] = dec_patterns[rng.randrange(len(dec_patterns))]
                else:
                    row['dec_data_in'] = rng.randrange(65536)
            elif mode < 85:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif mode < 92:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = enc_patterns[rng.randrange(len(enc_patterns))]
                row['dec_valid_in'] = 1
                row['dec_data_in'] = dec_patterns[rng.randrange(len(dec_patterns))]
            else:
                pass
        rows.append(row)
    return rows
