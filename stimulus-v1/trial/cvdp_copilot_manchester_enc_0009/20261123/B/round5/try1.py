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
            if mode < 20:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
            elif mode < 40:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif mode < 55:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif mode < 63:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xAA if (i & 1) else 0x55
            elif mode < 71:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0xAAAA if (i & 1) else 0x5555
            elif mode < 78:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0x0000 if (i & 1) else 0xFFFF
            elif mode < 84:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0xFF if (i & 1) else 0x00
            elif mode < 90:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.choice([0x0000, 0xFFFF, 0xAAAA, 0x5555, 0x00FF, 0xFF00])
            elif mode < 94:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = 0x0F if (i & 1) else 0xF0
            elif mode < 97:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = 0x0F0F if (i & 1) else 0xF0F0
            else:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
        rows.append(row)
    return rows
