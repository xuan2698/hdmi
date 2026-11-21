def stimulus(rng, cycles):
    rows = []
    rst_high = 3
    enc_pats = [0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x81, 0x18, 0x3C, 0xC3, 0x7E, 0xE7]
    dec_pats = [0x0000, 0xFFFF, 0xAAAA, 0x5555, 0x00FF, 0xFF00, 0x8001, 0x0180,
                0x3CC3, 0xC33C, 0x0F0F, 0xF0F0, 0x1234, 0xEDCB]
    for i in range(cycles):
        row = {
            'rst_in': 1 if i < rst_high else 0,
            'enc_valid_in': 0,
            'enc_data_in': 0,
            'dec_valid_in': 0,
            'dec_data_in': 0,
        }
        if i >= rst_high:
            phase = (i - rst_high) % 40
            if phase < 3:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = enc_pats[phase % len(enc_pats)]
            elif phase < 6:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = dec_pats[phase % len(dec_pats)]
            elif phase < 9:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif phase < 12:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xFF if (phase & 1) else 0x00
            elif phase < 15:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xFFFF if (phase & 1) else 0x0000
            elif phase < 18:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xAA if (phase & 1) else 0x55
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xAAAA if (phase & 1) else 0x5555
            elif phase < 22:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
            elif phase < 26:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif phase < 30:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = enc_pats[rng.randrange(len(enc_pats))]
                row['dec_valid_in'] = 1
                row['dec_data_in'] = dec_pats[rng.randrange(len(dec_pats))]
            elif phase < 34:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0x00
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0x0000
            elif phase < 37:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xFF
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xFFFF
            else:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
        rows.append(row)
    return rows
