def reference(vectors):
    mem = [0] * 8192
    aa = ea = ba = da = 0
    ab = eb = bb = db = 0
    oa = ob = 0
    res = []
    prev_clk = 0
    for i, row in enumerate(vectors):
        def g(k, d=0):
            if isinstance(row, dict):
                return row.get(k, d)
            return d
        pos = None
        if isinstance(row, dict) and 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                pos = e.lower().startswith('pos')
            else:
                pos = bool(e)
        elif isinstance(row, dict) and 'clk' in row:
            c = row['clk']
            pos = (prev_clk == 0 and c == 1)
            prev_clk = c
        else:
            pos = (i % 2 == 0)
        res.append({'data_out_a': oa & 0xFFFFFFFF, 'data_out_b': ob & 0xFFFFFFFF})
        if pos:
            noa = mem[aa] & 0xFFFFFFFF
            nob = mem[ab] & 0xFFFFFFFF
            if ea and eb and aa == ab:
                idx = aa
                w = mem[idx]
                for j in range(4):
                    m = 0xFF << (8 * j)
                    if (ba >> j) & 1:
                        w = (w & (~m & 0xFFFFFFFF)) | (da & m)
                    elif (bb >> j) & 1:
                        w = (w & (~m & 0xFFFFFFFF)) | (db & m)
                mem[idx] = w & 0xFFFFFFFF
            else:
                if ea:
                    idx = aa
                    w = mem[idx]
                    for j in range(4):
                        if (ba >> j) & 1:
                            m = 0xFF << (8 * j)
                            w = (w & (~m & 0xFFFFFFFF)) | (da & m)
                    mem[idx] = w & 0xFFFFFFFF
                if eb:
                    idx = ab
                    w = mem[idx]
                    for j in range(4):
                        if (bb >> j) & 1:
                            m = 0xFF << (8 * j)
                            w = (w & (~m & 0xFFFFFFFF)) | (db & m)
                    mem[idx] = w & 0xFFFFFFFF
            aa = g('addr_a') & 0x1FFF
            ea = g('en_a') & 1
            ba = g('be_a') & 0xF
            da = g('data_in_a') & 0xFFFFFFFF
            ab = g('addr_b') & 0x1FFF
            eb = g('en_b') & 1
            bb = g('be_b') & 0xF
            db = g('data_in_b') & 0xFFFFFFFF
            oa = noa
            ob = nob
    return res
