def stimulus(rng, cycles):
    rows = []
    rst_high = 3
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
            elif mode < 60:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xFF
            elif mode < 68:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0x00
            elif mode < 76:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xAAAA
            elif mode < 84:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0x5555
            elif mode < 90:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xFFFF
            elif mode < 94:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0x0000
            elif mode < 97:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xAAAA
            else:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
        rows.append(row)
    return rows
