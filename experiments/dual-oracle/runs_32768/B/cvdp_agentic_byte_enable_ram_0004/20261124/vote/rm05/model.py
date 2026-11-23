def reference(vectors):
    ram = [0] * 8192
    ra = rb = 0
    ea = eb = 0
    ba = bb = 0
    da = db = 0
    oa = ob = 0
    prev_clk = None
    out = []

    def val(r, k):
        if isinstance(r, dict):
            if k in r:
                return int(r[k])
            ku = k.upper()
            if ku in r:
                return int(r[ku])
        return 0

    for i, r in enumerate(vectors):
        pos = None
        if isinstance(r, dict):
            e = None
            for ek in ('edge', 'Edge', 'EDGE'):
                if ek in r:
                    e = r[ek]
                    break
            if e is not None:
                if isinstance(e, str):
                    el = e.lower()
                    pos = el.startswith('p') or el == '1' or el == 'true'
                else:
                    pos = bool(e)
            else:
                for pk in ('posedge', 'POSEDGE'):
                    if pk in r:
                        pos = bool(r[pk])
                        break
                if pos is None:
                    for nk in ('negedge', 'NEGEDGE'):
                        if nk in r:
                            pos = not bool(r[nk])
                            break

        if pos is None:
            if isinstance(r, dict) and ('clk' in r or 'CLK' in r):
                c = r.get('clk', r.get('CLK'))
                c = 1 if c else 0
                if prev_clk is None:
                    pos = (c == 1)
                else:
                    pos = (prev_clk == 0 and c == 1)
                prev_clk = c
            else:
                pos = (i % 2 == 0)

        if pos:
            out.append({'data_out_a': oa & 0xffffffff, 'data_out_b': ob & 0xffffffff})

            ca = val(r, 'addr_a') & 0x1fff
            cea = 1 if val(r, 'en_a') else 0
            cba = val(r, 'be_a') & 0xf
            cda = val(r, 'data_in_a') & 0xffffffff
            cb = val(r, 'addr_b') & 0x1fff
            ceb = 1 if val(r, 'en_b') else 0
            cbb = val(r, 'be_b') & 0xf
            cdb = val(r, 'data_in_b') & 0xffffffff

            noa = ram[ra & 0x1fff] & 0xffffffff
            nob = ram[rb & 0x1fff] & 0xffffffff

            if ea and eb and ((ra & 0x1fff) == (rb & 0x1fff)):
                idx = ra & 0x1fff
                nv = ram[idx]
                for j in range(4):
                    if (ba >> j) & 1:
                        mask = 0xff << (8 * j)
                        nv = (nv & ~mask) | (((da >> (8 * j)) & 0xff) << (8 * j))
                    elif (bb >> j) & 1:
                        mask = 0xff << (8 * j)
                        nv = (nv & ~mask) | (((db >> (8 * j)) & 0xff) << (8 * j))
                ram[idx] = nv & 0xffffffff
            else:
                if ea:
                    idx = ra & 0x1fff
                    nv = ram[idx]
                    for j in range(4):
                        if (ba >> j) & 1:
                            mask = 0xff << (8 * j)
                            nv = (nv & ~mask) | (((da >> (8 * j)) & 0xff) << (8 * j))
                    ram[idx] = nv & 0xffffffff
                if eb:
                    idx = rb & 0x1fff
                    nv = ram[idx]
                    for j in range(4):
                        if (bb >> j) & 1:
                            mask = 0xff << (8 * j)
                            nv = (nv & ~mask) | (((db >> (8 * j)) & 0xff) << (8 * j))
                    ram[idx] = nv & 0xffffffff

            ra, ea, ba, da = ca, cea, cba, cda
            rb, eb, bb, db = cb, ceb, cbb, cdb
            oa, ob = noa, nob
        else:
            out.append({'data_out_a': oa & 0xffffffff, 'data_out_b': ob & 0xffffffff})

    return out
