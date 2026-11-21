def stimulus(rng, cycles):
    rows = []
    # Manchester encode helper for 8-bit values
    def enc(v):
        out = 0
        for i in range(8):
            if (v >> i) & 1:
                out |= (1 << (2*i))       # 1 -> 01 (bit0=1, bit1=0)
            else:
                out |= (1 << (2*i + 1))   # 0 -> 10 (bit0=0, bit1=1)
        return out

    # Precompute some directed encoder patterns
    enc_patterns = [0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x01, 0x80, 0x7F, 0xFE]
    # Precompute decoder patterns: valid manchester, invalid, edge
    dec_patterns = [
        0x5AA5, 0xC33C, 0xAAAA, 0x5555, 0xFFFF, 0x0000,
        0x0F0F, 0xF0F0, 0x1234, 0xEDCB, 0x8001, 0x7FFE,
    ]

    for c in range(cycles):
        row = {}
        # Reset behavior: assert early, then occasionally
        if c < 2:
            row['rst_in'] = 1
        elif c % 97 == 0:
            row['rst_in'] = 1
        else:
            row['rst_in'] = 0

        # Encoder valid: toggle with some structure
        if c < 4:
            row['enc_valid_in'] = 0
        elif c % 7 == 0:
            row['enc_valid_in'] = 0
        else:
            row['enc_valid_in'] = 1

        # Encoder data: directed early, then mix
        if c < len(enc_patterns):
            row['enc_data_in'] = enc_patterns[c]
        elif c % 5 == 0:
            row['enc_data_in'] = (c * 37) & 0xFF
        elif c % 3 == 0:
            row['enc_data_in'] = rng.randrange(256)
        else:
            row['enc_data_in'] = (c & 0xFF)

        # Decoder valid: toggle differently from encoder
        if c < 3:
            row['dec_valid_in'] = 0
        elif c % 11 == 0:
            row['dec_valid_in'] = 0
        else:
            row['dec_valid_in'] = 1

        # Decoder data: mix valid manchester, invalid, random
        if c < len(dec_patterns):
            row['dec_data_in'] = dec_patterns[c]
        elif c % 4 == 0:
            # valid manchester of a random byte
            row['dec_data_in'] = enc(rng.randrange(256))
        elif c % 4 == 1:
            # invalid patterns
            row['dec_data_in'] = rng.choice([0xFFFF, 0x0000, 0xAAAA, 0x5555])
        elif c % 4 == 2:
            row['dec_data_in'] = rng.randrange(1 << 16)
        else:
            row['dec_data_in'] = (c * 0x1234) & 0xFFFF

        # Occasionally inject mid-cycle changes on data/valid
        if c % 13 == 5:
            mid = {}
            if rng.random() < 0.5:
                mid['enc_valid_in'] = 1 - row['enc_valid_in']
            if rng.random() < 0.5:
                mid['enc_data_in'] = rng.randrange(256)
            if rng.random() < 0.5:
                mid['dec_valid_in'] = 1 - row['dec_valid_in']
            if rng.random() < 0.5:
                mid['dec_data_in'] = rng.randrange(1 << 16)
            if mid:
                row['mid'] = mid

        rows.append(row)

    return rows
