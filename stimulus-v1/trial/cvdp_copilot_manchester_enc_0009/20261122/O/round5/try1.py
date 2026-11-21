def stimulus(rng, cycles):
    rows = []
    rst_high = 3
    enc_patterns = [0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x81, 0x18, 0x3C, 0xC3]
    dec_patterns = [0x0000, 0xFFFF, 0xAAAA, 0x5555, 0x00FF, 0xFF00, 0x8001, 0x0180, 0x3C3C, 0xC3C3]
    for i in range(cycles):
        row = {
            'rst_in': 1 if i < rst_high else 0,
            'enc_valid_in': 0,
            'enc_data_in': 0,
            'dec_valid_in': 0,
            'dec_data_in': 0,
        }
        if i >= rst_high:
            phase = (i - rst_high) % 24
            if phase < 2:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = enc_patterns[phase % len(enc_patterns)]
            elif phase < 4:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = dec_patterns[phase % len(dec_patterns)]
            elif phase < 6:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif phase < 8:
                pass
            elif phase < 10:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0x00
            elif phase < 12:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xFF
            elif phase < 14:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0x0000
            elif phase < 16:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xFFFF
            else:
                r = rng.random()
                if r < 0.30:
                    row['enc_valid_in'] = 1
                    row['enc_data_in'] = rng.randrange(256)
                elif r < 0.60:
                    row['dec_valid_in'] = 1
                    row['dec_data_in'] = rng.randrange(65536)
                elif r < 0.80:
                    row['enc_valid_in'] = 1
                    row['enc_data_in'] = rng.randrange(256)
                    row['dec_valid_in'] = 1
                    row['dec_data_in'] = rng.randrange(65536)
                else:
                    if rng.random() < 0.5:
                        row['enc_valid_in'] = 1
                        row['enc_data_in'] = rng.randrange(256)
                    else:
                        row['dec_valid_in'] = 1
                        row['dec_data_in'] = rng.randrange(65536)
        rows.append(row)
    return rows
