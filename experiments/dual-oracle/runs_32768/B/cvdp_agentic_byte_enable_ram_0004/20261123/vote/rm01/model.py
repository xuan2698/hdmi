def reference(vectors):
    XLEN = 32
    LINES = 8192
    ADDR_MASK = LINES - 1
    WORD_MASK = 0xffffffff
    BE_MASK = 0xf

    def num(v):
        if isinstance(v, str):
            return int(v, 0)
        return int(v)

    ram = [0] * LINES
    a_addr = a_en = a_be = a_data = 0
    b_addr = b_en = b_be = b_data = 0
    outs = []
    toggle = 1

    for row in vectors:
        if isinstance(row, dict):
            if 'edge' in row:
                e = row['edge']
            elif 'clk' in row:
                e = row['clk']
            elif 'posedge' in row:
                e = 'posedge' if row['posedge'] else 'negedge'
            else:
                e = None
        else:
            e = None

        if e is None:
            pos = (toggle == 1)
        else:
            if isinstance(e, str):
                el = e.lower()
                pos = el.startswith('pos') or el in ('1', 'p', 'true')
            else:
                pos = (e == 1)

        outs.append({
            'data_out_a': ram[a_addr & ADDR_MASK] & WORD_MASK,
            'data_out_b': ram[b_addr & ADDR_MASK] & WORD_MASK
        })

        if pos:
            def get(k, default=0):
                if isinstance(row, dict):
                    return row.get(k, default)
                return default

            ia = num(get('addr_a')) & ADDR_MASK
            ie = 1 if get('en_a') else 0
            ibe = num(get('be_a')) & BE_MASK
            ida = num(get('data_in_a')) & WORD_MASK

            ja = num(get('addr_b')) & ADDR_MASK
            je = 1 if get('en_b') else 0
            jbe = num(get('be_b')) & BE_MASK
            jdb = num(get('data_in_b')) & WORD_MASK

            if a_en and b_en and a_addr == b_addr:
                idx = a_addr & ADDR_MASK
                old = ram[idx]
                new = old
                for i in range(4):
                    sh = i * 8
                    m = 0xff << sh
                    if (a_be >> i) & 1:
                        v = (a_data >> sh) & 0xff
                        new = (new & ~m) | (v << sh)
                    elif (b_be >> i) & 1:
                        v = (b_data >> sh) & 0xff
                        new = (new & ~m) | (v << sh)
                ram[idx] = new & WORD_MASK
            else:
                if a_en:
                    idx = a_addr & ADDR_MASK
                    new = ram[idx]
                    for i in range(4):
                        if (a_be >> i) & 1:
                            sh = i * 8
                            v = (a_data >> sh) & 0xff
                            new = (new & ~(0xff << sh)) | (v << sh)
                    ram[idx] = new & WORD_MASK
                if b_en:
                    idx = b_addr & ADDR_MASK
                    new = ram[idx]
                    for i in range(4):
                        if (b_be >> i) & 1:
                            sh = i * 8
                            v = (b_data >> sh) & 0xff
                            new = (new & ~(0xff << sh)) | (v << sh)
                    ram[idx] = new & WORD_MASK

            a_addr, a_en, a_be, a_data = ia, ie, ibe, ida
            b_addr, b_en, b_be, b_data = ja, je, jbe, jdb

        if e is None:
            toggle = 0 if pos else 1

    return outs
