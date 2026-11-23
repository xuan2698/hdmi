def reference(vectors):
    MASK_ADDR = 8191
    MASK32 = 0xFFFFFFFF
    ram = [0] * 8192

    ar = br = 0
    ena = enb = 0
    bea = beb = 0
    da = db = 0

    ca = cb = 0
    cena = cenb = 0
    cbea = cbeb = 0
    cda = cdb = 0

    outs = []

    for i, row in enumerate(vectors):
        if 'addr_a' in row:
            ca = row['addr_a'] & MASK_ADDR
        if 'en_a' in row:
            cena = row['en_a'] & 1
        if 'be_a' in row:
            cbea = row['be_a'] & 0xF
        if 'data_in_a' in row:
            cda = row['data_in_a'] & MASK32

        if 'addr_b' in row:
            cb = row['addr_b'] & MASK_ADDR
        if 'en_b' in row:
            cenb = row['en_b'] & 1
        if 'be_b' in row:
            cbeb = row['be_b'] & 0xF
        if 'data_in_b' in row:
            cdb = row['data_in_b'] & MASK32

        ev = row.get('edge', row.get('Edge', None))
        if ev is None:
            pos = (i % 2 == 0)
        else:
            if isinstance(ev, str):
                s = ev.lower()
                if 'pos' in s:
                    pos = True
                elif 'neg' in s:
                    pos = False
                else:
                    pos = (i % 2 == 0)
            else:
                pos = bool(ev)

        outs.append({
            'data_out_a': ram[ar & MASK_ADDR] & MASK32,
            'data_out_b': ram[br & MASK_ADDR] & MASK32
        })

        if pos:
            if ena and enb and ar == br:
                a_addr = ar & MASK_ADDR
                word = ram[a_addr]
                for b in range(4):
                    sh = b * 8
                    if (bea >> b) & 1:
                        word = (word & ~(0xFF << sh)) | (((da >> sh) & 0xFF) << sh)
                    elif (beb >> b) & 1:
                        word = (word & ~(0xFF << sh)) | (((db >> sh) & 0xFF) << sh)
                ram[a_addr] = word & MASK32
            else:
                if ena:
                    a_addr = ar & MASK_ADDR
                    word = ram[a_addr]
                    for b in range(4):
                        if (bea >> b) & 1:
                            sh = b * 8
                            word = (word & ~(0xFF << sh)) | (((da >> sh) & 0xFF) << sh)
                    ram[a_addr] = word & MASK32

                if enb:
                    b_addr = br & MASK_ADDR
                    word = ram[b_addr]
                    for b in range(4):
                        if (beb >> b) & 1:
                            sh = b * 8
                            word = (word & ~(0xFF << sh)) | (((db >> sh) & 0xFF) << sh)
                    ram[b_addr] = word & MASK32

            ar, br = ca, cb
            ena, enb = cena, cenb
            bea, beb = cbea, cbeb
            da, db = cda, cdb

    return outs
