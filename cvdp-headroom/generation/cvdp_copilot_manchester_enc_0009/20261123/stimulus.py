def stimulus(rng, cycles):
    rows = []
    enc_pats = [0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x81, 0x7E, 0x01, 0x80]
    dec_pats = [0x0000, 0xFFFF, 0x5AA5, 0xC33C, 0xAAAA, 0x5555, 0x0F0F, 0xF0F0,
                0x00FF, 0xFF00, 0x1234, 0xEDCB, 0x8001, 0x7FFE]
    for c in range(cycles):
        rst = 0
        if c < 3:
            rst = 1
        elif c in (50, 51, 200, 201, 500, 501, 900, 901, 1400, 1401, 1800, 1801):
            rst = 1
        elif rng.random() < 0.01:
            rst = 1

        if rst:
            ev = rng.randint(0, 1)
            dv = rng.randint(0, 1)
            ed = rng.randint(0, 255)
            dd = rng.randint(0, 65535)
        else:
            phase = c % 16
            if phase < 4:
                ev = 1
                dv = 1
                ed = enc_pats[(c // 4) % len(enc_pats)]
                dd = dec_pats[(c // 4) % len(dec_pats)]
            elif phase < 8:
                ev = 1
                dv = 0
                ed = (c * 37) & 0xFF
                dd = (c * 1234) & 0xFFFF
            elif phase < 12:
                ev = 0
                dv = 1
                ed = rng.randint(0, 255)
                dd = rng.randint(0, 65535)
            else:
                ev = rng.randint(0, 1)
                dv = rng.randint(0, 1)
                ed = rng.randint(0, 255)
                dd = rng.randint(0, 65535)

        row = {
            'rst_in': rst,
            'enc_valid_in': ev,
            'enc_data_in': ed,
            'dec_valid_in': dv,
            'dec_data_in': dd,
        }
        if rng.random() < 0.15:
            mid = {}
            if rng.random() < 0.5:
                mid['enc_valid_in'] = rng.randint(0, 1)
            if rng.random() < 0.5:
                mid['dec_valid_in'] = rng.randint(0, 1)
            if rng.random() < 0.3:
                mid['enc_data_in'] = rng.randint(0, 255)
            if rng.random() < 0.3:
                mid['dec_data_in'] = rng.randint(0, 65535)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows
