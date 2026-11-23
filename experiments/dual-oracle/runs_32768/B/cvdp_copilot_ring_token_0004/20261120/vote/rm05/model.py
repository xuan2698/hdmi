def reference(vectors):
    def parse_edge(val):
        if isinstance(val, str):
            s = val.lower()
            if 'pos' in s or 'rise' in s or s == '1' or 'high' in s:
                return True
            if 'neg' in s or 'fall' in s or s == '0' or 'low' in s:
                return False
            return True
        try:
            return int(val) != 0
        except:
            return True

    def get(row, names, default=None):
        if isinstance(row, dict):
            for k in row:
                if isinstance(k, str):
                    lk = k.lower()
                    for n in names:
                        if lk == n.lower():
                            return row[k]
        return default

    state = 1
    result = []
    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            rst = int(get(row, ['rst', 'reset'], 0) or 0) & 1
            data_in = int(get(row, ['data_in', 'data'], 0) or 0) & 15
            has = int(get(row, ['has_data_to_send', 'has_data', 'send'], 0) or 0) & 1
            ev = get(row, ['edge', 'clk_edge', 'event', 'ev', 'posedge', 'negedge', 'clk', 'clock'], None)
            pos = (i % 2 == 0) if ev is None else parse_edge(ev)
        else:
            vals = list(row) if isinstance(row, (list, tuple)) else [row]
            rst = 0
            data_in = 0
            has = 0
            edge_found = False
            for j, v in enumerate(vals):
                if isinstance(v, str) and ('pos' in v.lower() or 'neg' in v.lower() or 'rise' in v.lower() or 'fall' in v.lower()):
                    pos = parse_edge(v)
                    rest = vals[:j] + vals[j+1:]
                    if len(rest) >= 3:
                        rst = int(rest[0]) & 1
                        data_in = int(rest[1]) & 15
                        has = int(rest[2]) & 1
                    elif len(rest) == 2:
                        rst = int(rest[0]) & 1
                        data_in = int(rest[1]) & 15
                    edge_found = True
                    break
            if not edge_found:
                if len(vals) >= 4:
                    rst = int(vals[0]) & 1
                    data_in = int(vals[1]) & 15
                    has = int(vals[2]) & 1
                    pos = parse_edge(vals[3])
                elif len(vals) == 3:
                    rst = int(vals[0]) & 1
                    data_in = int(vals[1]) & 15
                    has = int(vals[2]) & 1
                    pos = (i % 2 == 0)
                elif len(vals) == 2:
                    rst = int(vals[0]) & 1
                    data_in = int(vals[1]) & 15
                    pos = (i % 2 == 0)
                elif len(vals) == 1:
                    rst = int(vals[0]) & 1
                    pos = (i % 2 == 0)
                else:
                    pos = (i % 2 == 0)

        if rst:
            state = 1

        if rst:
            tr = 1
            tok = 0
            data_out = 0
        else:
            tr = state & 15
            if state == 1:
                tok = 2
            elif state == 2:
                tok = 4
            elif state == 4:
                tok = 8
            elif state == 8:
                tok = 1
            else:
                tok = 0
            if has and (state == 1 or state == 2 or state == 4 or state == 8):
                data_out = data_in & 15
            else:
                data_out = 0

        result.append({
            'data_out': data_out & 15,
            'token_received': tr & 15,
            'token': tok & 15
        })

        if pos:
            if rst:
                state = 1
            else:
                if state == 1:
                    state = 2
                elif state == 2:
                    state = 4
                elif state == 4:
                    state = 8
                elif state == 8:
                    state = 1
                else:
                    state = 1

    return result
