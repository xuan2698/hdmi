def stimulus(rng, cycles):
    rows = []
    rst_high = 5
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
            if mode < 30:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
            elif mode < 60:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif mode < 80:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif mode < 88:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xAA if (i & 1) else 0x55
            elif mode < 95:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xAAAA if (i & 1) else 0x5555
            elif mode < 98:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0x0000 if (i & 1) else 0xFFFF
            else:
                pass
        rows.append(row)
    return rows
