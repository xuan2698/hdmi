def reference(vectors):
    ram = [0] * 8192
    sa = sb = 0
    sea = seb = 0
    sba = sbb = 0
    sda = sdb = 0
    ca = cb = 0
    cea = ceb = 0
    cba = cbb = 0
    cda = cdb = 0
    oa = ob = 0
    res = []
    prev_clk = None
    idx = 0

    for row in vectors:
        ca = row.get('addr_a', ca) & 8191
        cb = row.get('addr_b', cb) & 8191
        cea = row.get('en_a', cea) & 1
        ceb = row.get('en_b', ceb) & 1
        cba = row.get('be_a', cba) & 15
        cbb = row.get('be_b', cbb) & 15
        cda = row.get('data_in_a', cda) & 0xffffffff
        cdb = row.get('data_in_b', cdb) & 0xffffffff

        e = row.get('edge', None)
        c = row.get('clk', None)

        if e is not None:
            if isinstance(e, str):
                es = e.lower()
                is_pos = es.startswith('pos') or es in ('1', 'rise', 'rising')
            else:
                is_pos = (e == 1 or e is True)
            if c is not None:
                prev_clk = c & 1
        elif c is not None:
            c = c & 1
            if prev_clk is None:
                is_pos = (c == 1)
            else:
                is_pos = (prev_clk == 0 and c == 1)
            prev_clk = c
        else:
            p = row.get('posedge', None)
            if p is not None:
                is_pos = bool(p)
            else:
                is_pos = (idx % 2 == 0)

        res.append({'data_out_a': oa & 0xffffffff, 'data_out_b': ob & 0xffffffff})

        if is_pos:
            noa = ram[sa] & 0xffffffff
            nob = ram[sb] & 0xffffffff

            if sea and seb and sa == sb:
                val = ram[sa] & 0xffffffff
                for i in range(4):
                    sh = i * 8
                    mask = 255 << sh
                    if (sba >> i) & 1:
                        val = (val & ~mask) | (((sda >> sh) & 255) << sh)
                    elif (sbb >> i) & 1:
                        val = (val & ~mask) | (((sdb >> sh) & 255) << sh)
                ram[sa] = val & 0xffffffff
            else:
                if sea:
                    val = ram[sa] & 0xffffffff
                    for i in range(4):
                        sh = i * 8
                        mask = 255 << sh
                        if (sba >> i) & 1:
                            val = (val & ~mask) | (((sda >> sh) & 255) << sh)
                    ram[sa] = val & 0xffffffff

                if seb:
                    val = ram[sb] & 0xffffffff
                    for i in range(4):
                        sh = i * 8
                        mask = 255 << sh
                        if (sbb >> i) & 1:
                            val = (val & ~mask) | (((sdb >> sh) & 255) << sh)
                    ram[sb] = val & 0xffffffff

            sa = ca
            sb = cb
            sea = cea
            seb = ceb
            sba = cba
            sbb = cbb
            sda = cda
            sdb = cdb
            oa = noa
            ob = nob

        idx += 1

    return res
