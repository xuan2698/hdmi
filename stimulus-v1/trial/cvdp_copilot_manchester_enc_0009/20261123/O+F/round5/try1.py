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
            if mode < 22:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
            elif mode < 44:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif mode < 62:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif mode < 66:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xAAAA
            elif mode < 70:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0x5555
            elif mode < 73:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xFFFF
            elif mode < 76:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0x0000
            elif mode < 79:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xFF
            elif mode < 82:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0x00
            elif mode < 85:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xAA
            elif mode < 88:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0x55
            elif mode < 91:
                row['rst_in'] = 1
            elif mode < 94:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0x8001
            elif mode < 97:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0x7FFE
            else:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xAAAA
        rows.append(row)
    return rows
