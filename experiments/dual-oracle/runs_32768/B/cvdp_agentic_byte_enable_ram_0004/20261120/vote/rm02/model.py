def reference(vectors):
    MASK = 0xFFFFFFFF
    LINES = 8192
    AMASK = LINES - 1
    mem = [0] * LINES

    st_addr_a = 0
    st_en_a = 0
    st_be_a = 0
    st_data_a = 0
    st_addr_b = 0
    st_en_b = 0
    st_be_b = 0
    st_data_b = 0

    latest_addr_a = 0
    latest_en_a = 0
    latest_be_a = 0
    latest_data_a = 0
    latest_addr_b = 0
    latest_en_b = 0
    latest_be_b = 0
    latest_data_b = 0

    out_a = 0
    out_b = 0
    outs = []
    prev_clk = None

    def vi(v):
        if isinstance(v, str):
            s = v.lower()
            if 'pos' in s:
                return 1
            if 'neg' in s:
                return 0
            try:
                return int(v, 0)
            except:
                return int(v)
        return int(v)

    for row in vectors:
        if 'addr_a' in row:
            latest_addr_a = vi(row['addr_a']) & AMASK
        if 'en_a' in row:
            latest_en_a = vi(row['en_a']) & 1
        if 'be_a' in row:
            latest_be_a = vi(row['be_a']) & 0xF
        if 'data_in_a' in row:
            latest_data_a = vi(row['data_in_a']) & MASK
        if 'addr_b' in row:
            latest_addr_b = vi(row['addr_b']) & AMASK
        if 'en_b' in row:
            latest_en_b = vi(row['en_b']) & 1
        if 'be_b' in row:
            latest_be_b = vi(row['be_b']) & 0xF
        if 'data_in_b' in row:
            latest_data_b = vi(row['data_in_b']) & MASK

        pos = False
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                s = e.lower()
                pos = ('pos' in s) or s == '1' or s == 'true'
            else:
                pos = bool(vi(e))
        else:
            cval = None
            if 'clk' in row:
                cval = row['clk']
            elif 'CLK' in row:
                cval = row['CLK']

            if cval is not None:
                if isinstance(cval, str) and ('pos' in cval.lower() or 'neg' in cval.lower()):
                    pos = 'pos' in cval.lower()
                    c = 1 if pos else 0
                else:
                    c = vi(cval) & 1
                    pos = (c == 1 and prev_clk != 1)
                prev_clk = c
            else:
                pos = (prev_clk is None or prev_clk == 0)
                prev_clk = 1 if pos else 0

        outs.append({'data_out_a': out_a & MASK, 'data_out_b': out_b & MASK})

        if pos:
            a_addr = st_addr_a
            b_addr = st_addr_b
            read_a = mem[a_addr] if 0 <= a_addr < LINES else 0
            read_b = mem[b_addr] if 0 <= b_addr < LINES else 0

            if st_en_a and st_en_b and a_addr == b_addr and 0 <= a_addr < LINES:
                old = mem[a_addr]
                new = old
                for i in range(4):
                    sh = i * 8
                    bm = 1 << i
                    clear = MASK ^ (0xFF << sh)
                    if st_be_a & bm:
                        new = (new & clear) | (((st_data_a >> sh) & 0xFF) << sh)
                    elif st_be_b & bm:
                        new = (new & clear) | (((st_data_b >> sh) & 0xFF) << sh)
                mem[a_addr] = new & MASK
            else:
                if st_en_a and 0 <= a_addr < LINES:
                    old = mem[a_addr]
                    new = old
                    for i in range(4):
                        sh = i * 8
                        bm = 1 << i
                        if st_be_a & bm:
                            clear = MASK ^ (0xFF << sh)
                            new = (new & clear) | (((st_data_a >> sh) & 0xFF) << sh)
                    mem[a_addr] = new & MASK

                if st_en_b and 0 <= b_addr < LINES:
                    old = mem[b_addr]
                    new = old
                    for i in range(4):
                        sh = i * 8
                        bm = 1 << i
                        if st_be_b & bm:
                            clear = MASK ^ (0xFF << sh)
                            new = (new & clear) | (((st_data_b >> sh) & 0xFF) << sh)
                    mem[b_addr] = new & MASK

            out_a = read_a & MASK
            out_b = read_b & MASK

            st_addr_a = latest_addr_a
            st_en_a = latest_en_a
            st_be_a = latest_be_a
            st_data_a = latest_data_a
            st_addr_b = latest_addr_b
            st_en_b = latest_en_b
            st_be_b = latest_be_b
            st_data_b = latest_data_b

    return outs
