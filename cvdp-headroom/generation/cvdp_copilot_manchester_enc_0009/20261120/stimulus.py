def stimulus(rng, cycles):
    rows = []
    enc_pat = [0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x81, 0x7E]
    dec_pat = [0x5AA5, 0xC33C, 0xFFFF, 0x0000, 0xAAAA, 0x5555, 0x0FF0, 0xF00F]
    for i in range(cycles):
        rst = 0
        # Reset pulses at start and periodically
        if i < 2 or (i % 97 == 0) or (i % 131 == 5):
            rst = 1
        # Encoder stimulus
        ev = 0
        ed = 0
        if not rst:
            if i % 7 == 0:
                ev = 1
                ed = enc_pat[(i // 7) % len(enc_pat)]
            elif i % 5 == 0:
                ev = 1
                ed = (i * 37) & 0xFF
            elif i % 3 == 0:
                ev = 1
                ed = rng.randrange(256)
            elif i % 11 == 1:
                ev = 0
                ed = rng.randrange(256)
            else:
                ev = rng.randrange(2)
                ed = rng.randrange(256)
        # Decoder stimulus
        dv = 0
        dd = 0
        if not rst:
            if i % 6 == 0:
                dv = 1
                dd = dec_pat[(i // 6) % len(dec_pat)]
            elif i % 4 == 0:
                dv = 1
                dd = (i * 0x1234) & 0xFFFF
            elif i % 9 == 2:
                dv = 1
                dd = rng.randrange(65536)
            elif i % 13 == 3:
                dv = 0
                dd = rng.randrange(65536)
            else:
                dv = rng.randrange(2)
                dd = rng.randrange(65536)
        row = {
            'rst_in': rst,
            'enc_valid_in': ev,
            'enc_data_in': ed,
            'dec_valid_in': dv,
            'dec_data_in': dd,
        }
        # Mid-cycle changes occasionally
        if not rst and i % 17 == 8:
            row['mid'] = {
                'enc_valid_in': rng.randrange(2),
                'enc_data_in': rng.randrange(256),
                'dec_valid_in': rng.randrange(2),
                'dec_data_in': rng.randrange(65536),
            }
        rows.append(row)
    return rows
