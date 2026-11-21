def stimulus(rng, cycles):
    rows = []
    # Manchester encode helper
    def enc(v):
        r = 0
        for i in range(8):
            if (v >> i) & 1:
                r |= (1 << (2*i))       # 1 -> 01 (bit0=1, bit1=0)
            else:
                r |= (1 << (2*i + 1))   # 0 -> 10 (bit0=0, bit1=1)
        return r

    # Directed encoder data patterns
    enc_pats = [0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x01, 0x80, 0x7F, 0xFE]
    # Directed decoder data patterns (valid + invalid)
    dec_pats = [0x5AA5, 0xC33C, 0xFFFF, 0x0000, 0xAAAA, 0x5555, 0x0FF0, 0xF00F]

    for c in range(cycles):
        row = {}
        # Reset schedule: assert early, and periodically
        if c < 3:
            rst = 1
        elif c % 97 == 0:
            rst = 1
        elif c % 97 == 1:
            rst = 1
        else:
            rst = 0
        row['rst_in'] = rst

        # Encoder valid: mostly on, with gaps
        if c < 3:
            ev = 0
        elif c % 13 == 0:
            ev = 0
        elif c % 7 == 0:
            ev = 1
        else:
            ev = 1 if (c % 3 != 2) else 0
        row['enc_valid_in'] = ev

        # Encoder data selection
        if c < 3:
            ed = 0
        elif c < 3 + len(enc_pats):
            ed = enc_pats[c - 3]
        elif c % 11 == 0:
            ed = (c * 37) & 0xFF
        elif c % 5 == 0:
            ed = rng.randrange(256)
        elif c % 4 == 0:
            ed = (c) & 0xFF
        else:
            ed = rng.randrange(256)
        row['enc_data_in'] = ed

        # Decoder valid
        if c < 3:
            dv = 0
        elif c % 17 == 0:
            dv = 0
        elif c % 9 == 0:
            dv = 1
        else:
            dv = 1 if (c % 2 == 0) else 0
        row['dec_valid_in'] = dv

        # Decoder data selection
        if c < 3:
            dd = 0
        elif c < 3 + len(dec_pats):
            dd = dec_pats[c - 3]
        elif c % 19 == 0:
            # feed encoded version of some value (valid manchester)
            dd = enc(rng.randrange(256))
        elif c % 6 == 0:
            dd = rng.randrange(65536)
        elif c % 4 == 1:
            dd = (c * 257) & 0xFFFF
        else:
            dd = rng.randrange(65536)
        row['dec_data_in'] = dd

        # Mid-cycle changes on some rows to exercise edge behavior
        if c % 23 == 5:
            mid = {}
            mid['enc_valid_in'] = 1 - row['enc_valid_in']
            mid['enc_data_in'] = rng.randrange(256)
            row['mid'] = mid
        elif c % 31 == 7:
            mid = {}
            mid['dec_valid_in'] = 1 - row['dec_valid_in']
            mid['dec_data_in'] = rng.randrange(65536)
            row['mid'] = mid
        elif c % 41 == 11:
            mid = {}
            mid['rst_in'] = 1
            row['mid'] = mid

        rows.append(row)

    return rows
