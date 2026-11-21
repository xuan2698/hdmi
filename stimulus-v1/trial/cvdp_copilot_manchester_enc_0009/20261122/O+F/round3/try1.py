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
            if r < 0.35:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
            elif r < 0.70:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif r < 0.85:
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
        if i == rst_high + 5:
            row['mid'] = {'rst_in': 1, 'enc_valid_in': 0, 'enc_data_in': 0,
                          'dec_valid_in': 0, 'dec_data_in': 0}
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
        if i == rst_high + 60:
            row['mid'] = {'rst_in': 1, 'enc_valid_in': 0, 'enc_data_in': 0,
                          'dec_valid_in': 0, 'dec_data_in': 0}
        if i == rst_high + 61:
            row['rst_in'] = 0
        rows.append(row)
    return rows
