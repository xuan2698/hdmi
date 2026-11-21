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
            if r < 0.40:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
            elif r < 0.80:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif r < 0.90:
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
        rows.append(row)
    return rows
