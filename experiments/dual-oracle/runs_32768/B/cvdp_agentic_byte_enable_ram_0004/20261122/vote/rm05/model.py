def reference(vectors):
    ram = {}
    MASK = 0xFFFFFFFF
    AMASK = 8191
    a_addr_r = b_addr_r = 0
    a_en_r = b_en_r = 0
    a_be_r = b_be_r = 0
    a_din_r = b_din_r = 0
    a_out = b_out = 0
    res = []
    for i, r in enumerate(vectors):
        res.append({'data_out_a': a_out & MASK, 'data_out_b': b_out & MASK})
        if i % 2 == 0:
            read_a = ram.get(a_addr_r, 0)
            read_b = ram.get(b_addr_r, 0)
            if a_en_r and b_en_r and a_addr_r == b_addr_r:
                addr = a_addr_r
                base = ram.get(addr, 0)
                nw = base
                for j in range(4):
                    sh = j * 8
                    if (a_be_r >> j) & 1:
                        nw = (nw & ~(0xFF << sh)) | (((a_din_r >> sh) & 0xFF) << sh)
                    elif (b_be_r >> j) & 1:
                        nw = (nw & ~(0xFF << sh)) | (((b_din_r >> sh) & 0xFF) << sh)
                if a_be_r or b_be_r:
                    ram[addr] = nw & MASK
            else:
                if a_en_r:
                    addr = a_addr_r
                    base = ram.get(addr, 0)
                    nw = base
                    for j in range(4):
                        if (a_be_r >> j) & 1:
                            sh = j * 8
                            nw = (nw & ~(0xFF << sh)) | (((a_din_r >> sh) & 0xFF) << sh)
                    if a_be_r:
                        ram[addr] = nw & MASK
                if b_en_r:
                    addr = b_addr_r
                    base = ram.get(addr, 0)
                    nw = base
                    for j in range(4):
                        if (b_be_r >> j) & 1:
                            sh = j * 8
                            nw = (nw & ~(0xFF << sh)) | (((b_din_r >> sh) & 0xFF) << sh)
                    if b_be_r:
                        ram[addr] = nw & MASK
            a_out = read_a & MASK
            b_out = read_b & MASK
            a_addr_r = r.get('addr_a', a_addr_r) & AMASK
            a_en_r = r.get('en_a', a_en_r) & 1
            a_be_r = r.get('be_a', a_be_r) & 0xF
            a_din_r = r.get('data_in_a', a_din_r) & MASK
            b_addr_r = r.get('addr_b', b_addr_r) & AMASK
            b_en_r = r.get('en_b', b_en_r) & 1
            b_be_r = r.get('be_b', b_be_r) & 0xF
            b_din_r = r.get('data_in_b', b_din_r) & MASK
    return res
