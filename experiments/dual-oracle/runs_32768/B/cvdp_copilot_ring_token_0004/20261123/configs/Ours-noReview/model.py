def reference(vectors):
    def nxt(s):
        if s == 1: return 2
        if s == 2: return 4
        if s == 4: return 8
        if s == 8: return 1
        return 1

    state = 1
    out = []
    prev_clk = None

    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            rst = int(row.get('rst', 0)) & 1
            data_in = int(row.get('data_in', 0)) & 0xF
            has = int(row.get('has_data_to_send', row.get('has_data', 0))) & 1
            edge = row.get('edge', row.get('edge_type', None))
            clk = row.get('clk', None)
        else:
            vals = list(row)
            if len(vals) >= 4:
                clk, rst, data_in, has = vals[0], vals[1], vals[2], vals[3]
            elif len(vals) == 3:
                clk = None
                rst, data_in, has = vals[0], vals[1], vals[2]
            else:
                clk, rst, data_in, has = None, 0, 0, 0
            edge = None
            rst = int(rst) & 1
            data_in = int(data_in) & 0xF
            has = int(has) & 1

        if clk is not None:
            clk = int(clk) & 1

        is_pos = False
        is_neg = False

        if edge is not None:
            e = str(edge).lower()
            if 'pos' in e or 'rise' in e or 'up' in e:
                is_pos = True
            elif 'neg' in e or 'fall' in e or 'down' in e:
                is_neg = True

        if not is_pos and not is_neg:
            if clk is not None:
                if prev_clk is None:
                    is_pos = clk == 1
                    is_neg = clk == 0
                else:
                    if prev_clk == 0 and clk == 1:
                        is_pos = True
                    elif prev_clk == 1 and clk == 0:
                        is_neg = True
                    else:
                        is_pos = clk == 1
                        is_neg = clk == 0
            else:
                is_pos = i % 2 == 0
                is_neg = not is_pos

        if rst:
            state = 1
            dout = 0
            tr = 1
            tok = 0
        else:
            tr = state & 0xF
            tok = nxt(state)
            dout = data_in if has else 0

        out.append({
            'data_out': dout & 0xF,
            'token_received': tr & 0xF,
            'token': tok & 0xF
        })

        if is_pos:
            if rst:
                state = 1
            else:
                state = nxt(state)

        if clk is not None:
            prev_clk = clk

    return out
