def reference(vectors):
    LINES = 8192
    MASK_ADDR = LINES - 1
    MASK_DATA = 0xFFFFFFFF
    MASK_BE = 0xF

    mem = [0] * LINES
    ar_a = en_a_r = be_a_r = di_a_r = 0
    ar_b = en_b_r = be_b_r = di_b_r = 0
    do_a = do_b = 0
    out = []

    def get(row, key, default=0):
        if isinstance(row, dict) and key in row:
            return row[key]
        return default

    def is_pos(row, idx):
        if isinstance(row, dict):
            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    l = e.lower()
                    if 'pos' in l or 'rise' in l:
                        return True
                    if 'neg' in l or 'fall' in l:
                        return False
                    try:
                        return int(l) == 1
                    except Exception:
                        return True
                return int(e) == 1
            if 'posedge' in row:
                return bool(row['posedge'])
            if 'negedge' in row:
                return not bool(row['negedge'])
            if 'clk' in row:
                c = row['clk']
                if isinstance(c, str):
                    l = c.lower()
                    if 'pos' in l or 'rise' in l:
                        return True
                    if 'neg' in l or 'fall' in l:
                        return False
                    try:
                        c = int(l)
                    except Exception:
                        return True
                return int(c) == 1
        return (idx % 2) == 0

    for idx, row in enumerate(vectors):
        out.append({'data_out_a': do_a & MASK_DATA, 'data_out_b': do_b & MASK_DATA})

        if is_pos(row, idx):
            ra = ar_a & MASK_ADDR
            rb = ar_b & MASK_ADDR
            nxt_a = mem[ra] & MASK_DATA
            nxt_b = mem[rb] & MASK_DATA

            updates = {}

            if en_a_r:
                ba = be_a_r & MASK_BE
                da = di_a_r & MASK_DATA
                aa = ar_a & MASK_ADDR
                if ba & 1:
                    updates[(aa, 0)] = da & 0xFF
                if ba & 2:
                    updates[(aa, 1)] = (da >> 8) & 0xFF
                if ba & 4:
                    updates[(aa, 2)] = (da >> 16) & 0xFF
                if ba & 8:
                    updates[(aa, 3)] = (da >> 24) & 0xFF

            if en_b_r:
                bb = be_b_r & MASK_BE
                db = di_b_r & MASK_DATA
                ab = ar_b & MASK_ADDR
                if bb & 1:
                    k = (ab, 0)
                    if k not in updates:
                        updates[k] = db & 0xFF
                if bb & 2:
                    k = (ab, 1)
                    if k not in updates:
                        updates[k] = (db >> 8) & 0xFF
                if bb & 4:
                    k = (ab, 2)
                    if k not in updates:
                        updates[k] = (db >> 16) & 0xFF
                if bb & 8:
                    k = (ab, 3)
                    if k not in updates:
                        updates[k] = (db >> 24) & 0xFF

            for (addr, bi), val in updates.items():
                sh = bi * 8
                mem[addr] = ((mem[addr] & (~(0xFF << sh) & MASK_DATA)) | ((val & 0xFF) << sh)) & MASK_DATA

            ar_a = int(get(row, 'addr_a', 0)) & MASK_ADDR
            en_a_r = int(get(row, 'en_a', 0)) & 1
            be_a_r = int(get(row, 'be_a', 0)) & MASK_BE
            di_a_r = int(get(row, 'data_in_a', 0)) & MASK_DATA

            ar_b = int(get(row, 'addr_b', 0)) & MASK_ADDR
            en_b_r = int(get(row, 'en_b', 0)) & 1
            be_b_r = int(get(row, 'be_b', 0)) & MASK_BE
            di_b_r = int(get(row, 'data_in_b', 0)) & MASK_DATA

            do_a = nxt_a & MASK_DATA
            do_b = nxt_b & MASK_DATA

    return out
