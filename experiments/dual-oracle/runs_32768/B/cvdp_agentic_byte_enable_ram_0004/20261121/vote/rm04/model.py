def reference(vectors):
    if isinstance(vectors, dict):
        n = 0
        for v in vectors.values():
            n = len(v)
            break
        rows = [{k: vectors[k][i] for k in vectors} for i in range(n)]
    else:
        rows = vectors

    LINES = 8192
    BYTES = 4
    ram = [0] * LINES
    a_addr = a_en = a_be = a_data = 0
    b_addr = b_en = b_be = b_data = 0
    out_a = out_b = 0
    res = []

    for idx, row in enumerate(rows):
        is_pos = None
        if 'clk' in row:
            clk = row['clk']
            if isinstance(clk, str):
                s = clk.lower()
                if 'pos' in s or s == '1' or s == 'true':
                    is_pos = True
                elif 'neg' in s or s == '0' or s == 'false':
                    is_pos = False
            else:
                is_pos = (clk == 1)
        if is_pos is None and 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                s = e.lower()
                if 'pos' in s:
                    is_pos = True
                elif 'neg' in s:
                    is_pos = False
        if is_pos is None:
            is_pos = (idx % 2 == 0)

        res.append({'data_out_a': out_a & 0xFFFFFFFF, 'data_out_b': out_b & 0xFFFFFFFF})

        if is_pos:
            ra = a_addr & (LINES - 1)
            rb = b_addr & (LINES - 1)
            noa = ram[ra]
            nob = ram[rb]

            if a_en and b_en and a_addr == b_addr:
                addr = a_addr & (LINES - 1)
                old = ram[addr]
                neww = old
                for i in range(BYTES):
                    bit = 1 << i
                    sh = 8 * i
                    mask = 0xFF << sh
                    if a_be & bit:
                        byte = (a_data >> sh) & 0xFF
                        neww = (neww & ~mask) | (byte << sh)
                    elif b_be & bit:
                        byte = (b_data >> sh) & 0xFF
                        neww = (neww & ~mask) | (byte << sh)
                ram[addr] = neww & 0xFFFFFFFF
            else:
                if a_en:
                    addr = a_addr & (LINES - 1)
                    old = ram[addr]
                    neww = old
                    for i in range(BYTES):
                        bit = 1 << i
                        sh = 8 * i
                        if a_be & bit:
                            byte = (a_data >> sh) & 0xFF
                            neww = (neww & ~(0xFF << sh)) | (byte << sh)
                    ram[addr] = neww & 0xFFFFFFFF
                if b_en:
                    addr = b_addr & (LINES - 1)
                    old = ram[addr]
                    neww = old
                    for i in range(BYTES):
                        bit = 1 << i
                        sh = 8 * i
                        if b_be & bit:
                            byte = (b_data >> sh) & 0xFF
                            neww = (neww & ~(0xFF << sh)) | (byte << sh)
                    ram[addr] = neww & 0xFFFFFFFF

            out_a = noa & 0xFFFFFFFF
            out_b = nob & 0xFFFFFFFF

            a_addr = row.get('addr_a', 0) & 0x1FFF
            a_en = row.get('en_a', 0) & 1
            a_be = row.get('be_a', 0) & 0xF
            a_data = row.get('data_in_a', 0) & 0xFFFFFFFF
            b_addr = row.get('addr_b', 0) & 0x1FFF
            b_en = row.get('en_b', 0) & 1
            b_be = row.get('be_b', 0) & 0xF
            b_data = row.get('data_in_b', 0) & 0xFFFFFFFF

    return res
