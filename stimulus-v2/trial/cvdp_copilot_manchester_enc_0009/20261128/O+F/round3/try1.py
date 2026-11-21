def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        rst = 1 if i < 3 else 0
        enc_valid = 0
        enc_data = 0
        dec_valid = 0
        dec_data = 0
        mid = None
        if rst == 0:
            if i >= 5:
                if rng.random() < 0.6:
                    enc_valid = 1
                    enc_data = rng.randrange(256)
                if rng.random() < 0.6:
                    dec_valid = 1
                    dec_data = rng.randrange(65536)
            if i == 6:
                mid = {'rst_in': 1, 'enc_valid_in': 0, 'enc_data_in': 0,
                       'dec_valid_in': 0, 'dec_data_in': 0}
            elif i == 8:
                mid = {'enc_valid_in': 1, 'enc_data_in': 22,
                       'dec_valid_in': 1, 'dec_data_in': 0}
        row = {
            'rst_in': rst,
            'enc_valid_in': enc_valid,
            'enc_data_in': enc_data,
            'dec_valid_in': dec_valid,
            'dec_data_in': dec_data,
        }
        if mid is not None:
            row['mid'] = mid
        rows.append(row)
    return rows
