def stimulus(rng, cycles):
    rows = []
    enc_pat = [0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x81, 0x7E]
    dec_pat = [0x5AA5, 0xC33C, 0xFFFF, 0x0000, 0xAAAA, 0x5555, 0x0FF0, 0xF00F]
    for i in range(cycles):
        rst = 0
        if i < 3:
            rst = 1
        elif i % 97 == 0:
            rst = 1
        elif i % 131 == 0:
            rst = 1
        ev = 0
        dv = 0
        ed = 0
        dd = 0
        if rst == 0:
            phase = i % 16
            if phase < 4:
                ev = 1
                ed = enc_pat[(i // 4) % len(enc_pat)]
            elif phase < 8:
                dv = 1
                dd = dec_pat[(i // 4) % len(dec_pat)]
            elif phase < 12:
                ev = 1
                dv = 1
                ed = (i * 37) & 0xFF
                dd = (i * 12345) & 0xFFFF
            else:
                ev = rng.randint(0, 1)
                dv = rng.randint(0, 1)
                ed = rng.randint(0, 255)
                dd = rng.randint(0, 65535)
            if i % 23 == 0:
                ev = 1
                ed = 0x00
            if i % 29 == 0:
                ev = 1
                ed = 0xFF
            if i % 31 == 0:
                dv = 1
                dd = 0xFFFF
            if i % 37 == 0:
                dv = 1
                dd = 0x0000
            if i % 41 == 0:
                ev = 1
                ed = 0xAA
            if i % 43 == 0:
                ev = 1
                ed = 0x55
        row = {
            'rst_in': rst,
            'enc_valid_in': ev,
            'enc_data_in': ed & 0xFF,
            'dec_valid_in': dv,
            'dec_data_in': dd & 0xFFFF,
        }
        if i % 7 == 3 and rst == 0:
            row['mid'] = {
                'enc_valid_in': rng.randint(0, 1),
                'dec_valid_in': rng.randint(0, 1),
                'enc_data_in': rng.randint(0, 255),
                'dec_data_in': rng.randint(0, 65535),
            }
        rows.append(row)
    return rows
