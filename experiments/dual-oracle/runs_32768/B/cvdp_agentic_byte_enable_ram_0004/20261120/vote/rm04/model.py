def reference(vectors):
    LINES = 8192
    MASK = 0xFFFFFFFF
    ADDR_MASK = LINES - 1
    ram = [0] * LINES
    sa = 0
    sea = 0
    sba = 0
    sda = 0
    sb = 0
    seb = 0
    sbb = 0
    sdb = 0
    oa = 0
    ob = 0
    inp = {
        'addr_a': 0, 'en_a': 0, 'be_a': 0, 'data_in_a': 0,
        'addr_b': 0, 'en_b': 0, 'be_b': 0, 'data_in_b': 0
    }
    res = []
    for idx, row in enumerate(vectors):
        for k in inp:
            if k in row:
                inp[k] = row[k]

        is_pos = None
        if 'edge' in row:
            ev = row['edge']
            if ev in (1, 'posedge', 'pos', 'rise', 'rising', True, '1'):
                is_pos = True
            elif ev in (0, -1, 'negedge', 'neg', 'fall', 'falling', False, '0'):
                is_pos = False
        if is_pos is None and 'clk' in row:
            cv = row['clk']
            if cv in (0, 1, False, True):
                is_pos = bool(cv)
        if is_pos is None:
            is_pos = (idx % 2 == 0)

        res.append({'data_out_a': oa & MASK, 'data_out_b': ob & MASK})

        if is_pos:
            a_en = sea & 1
            b_en = seb & 1
            a_addr = sa & ADDR_MASK
            b_addr = sb & ADDR_MASK
            a_be = sba & 0xF
            b_be = sbb & 0xF

            ra = ram[a_addr]
            rb = ram[b_addr]

            if a_en and b_en and (a_addr == b_addr):
                word = ram[a_addr]
                for i in range(4):
                    shift = i * 8
                    bit = 1 << i
                    if a_be & bit:
                        val = (sda >> shift) & 0xFF
                        word = (word & ~(0xFF << shift)) | (val << shift)
                    elif b_be & bit:
                        val = (sdb >> shift) & 0xFF
                        word = (word & ~(0xFF << shift)) | (val << shift)
                ram[a_addr] = word & MASK
            else:
                if a_en:
                    word = ram[a_addr]
                    for i in range(4):
                        shift = i * 8
                        if a_be & (1 << i):
                            val = (sda >> shift) & 0xFF
                            word = (word & ~(0xFF << shift)) | (val << shift)
                    ram[a_addr] = word & MASK
                if b_en:
                    word = ram[b_addr]
                    for i in range(4):
                        shift = i * 8
                        if b_be & (1 << i):
                            val = (sdb >> shift) & 0xFF
                            word = (word & ~(0xFF << shift)) | (val << shift)
                    ram[b_addr] = word & MASK

            oa = ra & MASK
            ob = rb & MASK

            sa = inp['addr_a'] & ADDR_MASK
            sea = inp['en_a'] & 1
            sba = inp['be_a'] & 0xF
            sda = inp['data_in_a'] & MASK
            sb = inp['addr_b'] & ADDR_MASK
            seb = inp['en_b'] & 1
            sbb = inp['be_b'] & 0xF
            sdb = inp['data_in_b'] & MASK

    return res
