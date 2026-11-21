def stimulus(rng, cycles):
    rows = []
    rst = 1
    ev = 0
    ed = 0
    dv = 0
    dd = 0
    for c in range(cycles):
        if c < 3:
            rst = 1
        else:
            rst = 0
        if rst:
            ev = 0
            ed = 0
            dv = 0
            dd = 0
        else:
            r = rng.random()
            if r < 0.45:
                ev = 1
                ed = rng.randrange(256)
            else:
                ev = 0
                ed = 0
            r2 = rng.random()
            if r2 < 0.45:
                dv = 1
                dd = rng.randrange(65536)
            else:
                dv = 0
                dd = 0
        row = {
            'rst_in': rst,
            'enc_valid_in': ev,
            'enc_data_in': ed,
            'dec_valid_in': dv,
            'dec_data_in': dd,
        }
        if c == 1:
            row['mid'] = {'rst_in': 1, 'enc_valid_in': 0, 'enc_data_in': 0, 'dec_valid_in': 0, 'dec_data_in': 0}
        elif c == 2:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 1, 'enc_data_in': 22, 'dec_valid_in': 1, 'dec_data_in': 0}
        elif c == 4:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 1, 'enc_data_in': 255, 'dec_valid_in': 1, 'dec_data_in': 64}
        elif c == 10:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 1, 'enc_data_in': 170, 'dec_valid_in': 1, 'dec_data_in': 43690}
        elif c == 50:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 1, 'enc_data_in': 85, 'dec_valid_in': 1, 'dec_data_in': 21845}
        elif c == 100:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 1, 'enc_data_in': 0, 'dec_valid_in': 1, 'dec_data_in': 65535}
        elif c == 200:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 1, 'enc_data_in': 255, 'dec_valid_in': 1, 'dec_data_in': 0}
        elif c == 500:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 1, 'enc_data_in': 165, 'dec_valid_in': 1, 'dec_data_in': 42405}
        elif c == 1000:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 1, 'enc_data_in': 90, 'dec_valid_in': 1, 'dec_data_in': 23130}
        elif c == 2000:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 1, 'enc_data_in': 195, 'dec_valid_in': 1, 'dec_data_in': 50055}
        elif c == 3000:
            row['mid'] = {'rst_in': 0, 'enc_valid_in': 1, 'enc_data_in': 60, 'dec_valid_in': 1, 'dec_data_in': 15420}
        rows.append(row)
    return rows
