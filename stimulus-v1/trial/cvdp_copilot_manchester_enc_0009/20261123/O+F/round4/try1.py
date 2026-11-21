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
            if mode < 25:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
            elif mode < 50:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif mode < 70:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif mode < 75:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xAAAA
            elif mode < 80:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0x5555
            elif mode < 83:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xFFFF
            elif mode < 86:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0x0000
            elif mode < 89:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xFF
            elif mode < 92:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0x00
            elif mode < 94:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xAA
            elif mode < 96:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0x55
            elif mode < 98:
                row['rst_in'] = 1
            else:
                pass
        rows.append(row)
    return rows
