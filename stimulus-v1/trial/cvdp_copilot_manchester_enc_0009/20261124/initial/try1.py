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
            if mode < 35:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
            elif mode < 70:
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            elif mode < 85:
                row['enc_valid_in'] = 1
                row['enc_data_in'] = rng.randrange(256)
                row['dec_valid_in'] = 1
                row['dec_data_in'] = rng.randrange(65536)
            else:
                if rng.randrange(2):
                    row['enc_valid_in'] = 1
                    row['enc_data_in'] = rng.randrange(256)
                else:
                    row['dec_valid_in'] = 1
                    row['dec_data_in'] = rng.randrange(65536)
        rows.append(row)
    return rows
