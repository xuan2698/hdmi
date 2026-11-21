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
            elif mode < 78:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xAA if (i & 1) else 0x55
            elif mode < 86:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xAAAA if (i & 1) else 0x5555
            elif mode < 92:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0x0000 if (i & 1) else 0xFFFF
            elif mode < 96:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xFF if (i & 1) else 0x00
            else:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.choice([0x0000, 0xFFFF, 0xAAAA, 0x5555, 0x00FF, 0xFF00])
        rows.append(row)
    return rows
