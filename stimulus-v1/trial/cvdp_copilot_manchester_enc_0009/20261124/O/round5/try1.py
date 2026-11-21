def stimulus(rng, cycles):
    rows = []
    rst_high = 4
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
            if mode < 18:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
            elif mode < 36:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif mode < 52:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif mode < 62:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.choice([0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x81, 0x7E])
            elif mode < 72:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.choice([0x0000, 0xFFFF, 0xAAAA, 0x5555, 0x00FF, 0xFF00, 0x8001, 0x7FFE])
            elif mode < 82:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif mode < 90:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0
            else:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0
        rows.append(row)
    return rows
