def reference(vectors):
    def gv(row, name, default=0):
        if name in row:
            return row[name]
        un = name.upper()
        if un in row:
            return row[un]
        return default

    def is_pos(row):
        for k in ('edge', 'Edge', 'EDGE', 'edge_type', 'edgeType', 'EdgeType'):
            if k in row:
                v = row[k]
                if isinstance(v, str):
                    s = v.lower()
                    if 'pos' in s or s in ('1', 'rise', 'rising'):
                        return True
                    if 'neg' in s or s in ('0', 'fall', 'falling'):
                        return False
                else:
                    return bool(int(v))
        for k in ('clk', 'Clk', 'CLK', 'clock', 'Clock', 'CLOCK'):
            if k in row:
                v = row[k]
                if isinstance(v, str):
                    s = v.lower()
                    if 'pos' in s or s in ('1', 'rise', 'rising'):
                        return True
                    if 'neg' in s or s in ('0', 'fall', 'falling'):
                        return False
                else:
                    return bool(int(v))
        return True

    wcp = 0
    pmp = 0
    lat = 0
    prev = 0
    out = []

    for row in vectors:
        reset = int(gv(row, 'reset', 0)) & 1
        if reset:
            wcp = 0
            pmp = 0
            lat = 0
            prev = 0

        out.append({
            'word_change_pulse': wcp,
            'pattern_match_pulse': pmp,
            'latched_pattern': lat & 0xFF
        })

        if is_pos(row) and not reset:
            data = int(gv(row, 'data_in', 0)) & 0xFF
            mask = int(gv(row, 'mask', 0xFF)) & 0xFF
            match_pattern = int(gv(row, 'match_pattern', 0)) & 0xFF
            enable = int(gv(row, 'enable', 0)) & 1
            latch_pattern = int(gv(row, 'latch_pattern', 0)) & 1

            change = ((data ^ prev) & mask) != 0
            match = (((data ^ lat) & mask) == 0)

            wcp = 1 if (enable and change) else 0
            pmp = 1 if (enable and match) else 0
            lat = (match_pattern if latch_pattern else lat) & 0xFF
            prev = data

    return out
