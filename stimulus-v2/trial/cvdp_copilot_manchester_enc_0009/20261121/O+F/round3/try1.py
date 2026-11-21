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
            if i < 10:
                enc_valid = 1
                enc_data = (1 << (i % 8)) & 0xFF
                dec_valid = 1
                dec_data = 0x5555 if (i % 2 == 0) else 0xAAAA
            elif i < 24:
                enc_valid = 1
                enc_data = rng.randrange(256)
                dec_valid = 1
                dec_data = rng.randrange(65536)
            else:
                r = rng.random()
                if r < 0.5:
                    enc_valid = 1
                    enc_data = rng.randrange(256)
                if rng.random() < 0.5:
                    dec_valid = 1
                    dec_data = rng.randrange(65536)
                if rng.random() < 0.12:
                    mid = {'rst_in': 1}
                elif rng.random() < 0.18:
                    mid = {'enc_valid_in': 1 - enc_valid}
                elif rng.random() < 0.18:
                    mid = {'dec_valid_in': 1 - dec_valid}
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
