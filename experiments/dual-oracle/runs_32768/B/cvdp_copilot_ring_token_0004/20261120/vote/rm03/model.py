def reference(vectors):
    node = 0
    out = []
    fallback_pos = True
    for row in vectors:
        if isinstance(row, dict):
            rst = int(row.get('rst', 0)) & 1
            data_in = int(row.get('data_in', 0)) & 0xF
            has = int(row.get('has_data_to_send', 0)) & 1
            is_pos = None
            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    s = e.lower()
                    if 'pos' in s:
                        is_pos = True
                    elif 'neg' in s:
                        is_pos = False
                    else:
                        try:
                            is_pos = int(e) != 0
                        except:
                            is_pos = bool(e)
                else:
                    is_pos = bool(e)
            elif 'clk' in row:
                c = row['clk']
                if isinstance(c, str):
                    s = c.lower()
                    if 'pos' in s:
                        is_pos = True
                    elif 'neg' in s:
                        is_pos = False
                    else:
                        try:
                            is_pos = int(c) != 0
                        except:
                            is_pos = bool(c)
                else:
                    is_pos = bool(c)
        else:
            vals = list(row)
            is_pos = None
            for i, v in enumerate(vals):
                if isinstance(v, str):
                    s = v.lower()
                    if 'pos' in s or 'neg' in s:
                        is_pos = 'pos' in s
                        vals.pop(i)
                        break
            if len(vals) >= 4:
                rst = int(vals[0]) & 1
                data_in = int(vals[1]) & 0xF
                has = int(vals[2]) & 1
                if is_pos is None:
                    is_pos = bool(vals[3])
            elif len(vals) == 3:
                rst = int(vals[0]) & 1
                data_in = int(vals[1]) & 0xF
                has = int(vals[2]) & 1
            elif len(vals) == 2:
                rst = int(vals[0]) & 1
                data_in = int(vals[1]) & 0xF
                has = 0
            else:
                rst = int(vals[0]) & 1 if vals else 0
                data_in = 0
                has = 0
        if is_pos is None:
            is_pos = fallback_pos
        fallback_pos = not is_pos
        if rst:
            node = 0
            tr = 0x1
            tok = 0x0
            dout = 0x0
        else:
            tr = 1 << node
            tok = 1 << ((node + 1) & 3)
            dout = (data_in & 0xF) if has else 0
        out.append({'data_out': dout, 'token_received': tr, 'token': tok})
        if is_pos and not rst:
            node = (node + 1) & 3
    return out
