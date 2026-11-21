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
            r = rng.random()
            if r < 0.28:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
            elif r < 0.56:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif r < 0.76:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif r < 0.86:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.choice([0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x81, 0x18])
            elif r < 0.94:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.choice([0x0000, 0xFFFF, 0xAAAA, 0x5555, 0x00FF, 0xFF00, 0x8118, 0x1881])
            else:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
        if i == rst_high + 5:
            row['mid'] = {'rst_in': 1, 'enc_valid_in': 0, 'enc_data_in': 0,
                          'dec_valid_in': 0, 'dec_data_in': 0}
        if i == rst_high + 6:
            row['rst_in'] = 0
        if i == rst_high + 20:
            row['mid'] = {'rst_in': 1, 'enc_valid_in': 0, 'enc_data_in': 0,
                          'dec_valid_in': 0, 'dec_data_in': 0}
        if i == rst_high + 21:
            row['rst_in'] = 0
        if i == rst_high + 40:
            row['enc_valid_in'] = 1
            row['enc_data_in'] = 0xAA
            row['dec_valid_in'] = 1
            row['dec_data_in'] = 0xAAAA
        if i == rst_high + 41:
            row['enc_valid_in'] = 1
            row['enc_data_in'] = 0x55
            row['dec_valid_in'] = 1
            row['dec_data_in'] = 0x5555
        if i == rst_high + 42:
            row['enc_valid_in'] = 1
            row['enc_data_in'] = 0xFF
            row['dec_valid_in'] = 1
            row['dec_data_in'] = 0xFFFF
        if i == rst_high + 43:
            row['enc_valid_in'] = 1
            row['enc_data_in'] = 0x00
            row['dec_valid_in'] = 1
            row['dec_data_in'] = 0x0000
        if i == rst_high + 44:
            row['enc_valid_in'] = 1
            row['enc_data_in'] = 0x0F
            row['dec_valid_in'] = 1
            row['dec_data_in'] = 0x00FF
        if i == rst_high + 45:
            row['enc_valid_in'] = 1
            row['enc_data_in'] = 0xF0
            row['dec_valid_in'] = 1
            row['dec_data_in'] = 0xFF00
        if i == rst_high + 60:
            row['mid'] = {'rst_in': 1, 'enc_valid_in': 0, 'enc_data_in': 0,
                          'dec_valid_in': 0, 'dec_data_in': 0}
        if i == rst_high + 61:
            row['rst_in'] = 0
        if i == rst_high + 80:
            row['enc_valid_in'] = 1
            row['enc_data_in'] = 0x81
            row['dec_valid_in'] = 1
            row['dec_data_in'] = 0x8118
        if i == rst_high + 81:
            row['enc_valid_in'] = 1
            row['enc_data_in'] = 0x18
            row['dec_valid_in'] = 1
            row['dec_data_in'] = 0x1881
        if i == rst_high + 100:
            row['enc_valid_in'] = 1
            row['enc_data_in'] = 0x00
            row['dec_valid_in'] = 1
            row['dec_data_in'] = 0x0000
        if i == rst_high + 101:
            row['enc_valid_in'] = 1
            row['enc_data_in'] = 0xFF
            row['dec_valid_in'] = 1
            row['dec_data_in'] = 0xFFFF
        if i == rst_high + 120:
            row['mid'] = {'rst_in': 1, 'enc_valid_in': 0, 'enc_data_in': 0,
                          'dec_valid_in': 0, 'dec_data_in': 0}
        if i == rst_high + 121:
            row['rst_in'] = 0
        if i == rst_high + 140:
            row['enc_valid_in'] = 1
            row['enc_data_in'] = 0x3C
            row['dec_valid_in'] = 1
            row['dec_data_in'] = 0x3C3C
        if i == rst_high + 141:
            row['enc_valid_in'] = 1
            row['enc_data_in'] = 0xC3
            row['dec_valid_in'] = 1
            row['dec_data_in'] = 0xC3C3
        rows.append(row)
    return rows
