def stimulus(rng, cycles):
    rows = []
    rst_high = 3
    enc_patterns = [0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x81, 0x18, 0x3C, 0xC3]
    dec_patterns = [0x0000, 0xFFFF, 0xAAAA, 0x5555, 0x00FF, 0xFF00, 0x8001, 0x0180, 0x0F0F, 0xF0F0]
    for i in range(cycles):
        row = {
            'rst_in': 1 if i < rst_high else 0,
            'enc_valid_in': 0,
            'enc_data_in': 0,
            'dec_valid_in': 0,
            'dec_data_in': 0,
        }
        if i >= rst_high:
            r = rng.random()
            if r < 0.35:
                row['enc_valid_in'] = 1
                if rng.random() < 0.5:
                    row['enc_data_in'] = rng.choice(enc_patterns)
                else:
                    row['enc_data_in'] = rng.randrange(256)
            elif r < 0.70:
                row['dec_valid_in'] = 1
                if rng.random() < 0.5:
                    row['dec_data_in'] = rng.choice(dec_patterns)
                else:
                    row['dec_data_in'] = rng.randrange(65536)
            elif r < 0.85:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif r < 0.92:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0
            else:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0
        rows.append(row)
    return rows
