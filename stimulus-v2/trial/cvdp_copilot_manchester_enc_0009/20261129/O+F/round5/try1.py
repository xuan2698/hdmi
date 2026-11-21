def stimulus(rng, cycles):
    rows = []
    rst = 1
    enc_valid = 0
    enc_data = 0
    dec_valid = 0
    dec_data = 0
    for i in range(cycles):
        if i < 2:
            rst = 1
            enc_valid = 0
            enc_data = 0
            dec_valid = 0
            dec_data = 0
        elif i < 4:
            rst = 0
            enc_valid = 0
            enc_data = 0
            dec_valid = 0
            dec_data = 0
        else:
            rst = 0
            if rng.random() < 0.45:
                enc_valid = 1
                enc_data = rng.randrange(256)
            else:
                enc_valid = 0
                enc_data = 0
            if rng.random() < 0.45:
                dec_valid = 1
                dec_data = rng.randrange(65536)
            else:
                dec_valid = 0
                dec_data = 0
        row = {
            'rst_in': rst,
            'enc_valid_in': enc_valid,
            'enc_data_in': enc_data,
            'dec_valid_in': dec_valid,
            'dec_data_in': dec_data,
        }
        if i == 1:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 1, 'enc_data_in': 0xAA,
                          'dec_valid_in': 1, 'dec_data_in': 0x5555}
        elif i == 2:
            row['mid'] = {'rst_in': 1, 'enc_valid_in': 0, 'enc_data_in': 0,
                          'dec_valid_in': 0, 'dec_data_in': 0}
        elif i == 5:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 1, 'enc_data_in': 0xFF,
                          'dec_valid_in': 1, 'dec_data_in': 0xAAAA}
        elif i == 8:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 0, 'enc_data_in': 0,
                          'dec_valid_in': 1, 'dec_data_in': 0x0000}
        elif i == 12:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 1, 'enc_data_in': 0x55,
                          'dec_valid_in': 1, 'dec_data_in': 0xFFFF}
        rows.append(row)
    return rows
