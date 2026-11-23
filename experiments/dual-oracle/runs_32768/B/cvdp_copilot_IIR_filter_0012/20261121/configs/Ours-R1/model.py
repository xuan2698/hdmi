def reference(vectors):
    def s16(v):
        v = int(v) & 0xFFFF
        if v & 0x8000:
            return v - 0x10000
        return v
    def sat(v):
        if v > 32767:
            v = 32767
        elif v < -32768:
            v = -32768
        return v & 0xFFFF
    coeffs = ((1, 2, 1, 2), (3, 2, -1, 2), (1, -1, 0, 1), (2, 3, 1, 3))
    out_1 = out_2 = out_3 = 0
    h1_1 = h1_2 = h2_1 = h2_2 = h3_1 = h3_2 = 0
    prev_clk = 0
    res = []
    for i, row in enumerate(vectors):
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                clk = 1 if 'pos' in e.lower() else 0
            else:
                clk = 1 if e else 0
        else:
            clk = row.get('clk', 1 if i % 2 == 0 else 0)
        is_pos = (clk == 1 and prev_clk == 0)
        reset = int(row.get('reset', 0))
        if reset == 1:
            out_1 = out_2 = out_3 = 0
            h1_1 = h1_2 = h2_1 = h2_2 = h3_1 = h3_2 = 0
        res.append({'out_1': out_1 & 0xFFFF, 'out_2': out_2 & 0xFFFF, 'out_3': out_3 & 0xFFFF})
        if reset == 0 and is_pos:
            x1 = s16(row.get('in_1', 0))
            x2 = s16(row.get('in_2', 0))
            x3 = s16(row.get('in_3', 0))
            sel = int(row.get('filter_select', 0)) & 3
            a, b, c, sh = coeffs[sel]
            out_1 = sat((a * x1 + b * h1_1 + c * h1_2) >> sh)
            out_2 = sat((a * x2 + b * h2_1 + c * h2_2) >> sh)
            out_3 = sat((a * x3 + b * h3_1 + c * h3_2) >> sh)
            h1_2 = h1_1
            h1_1 = x1
            h2_2 = h2_1
            h2_1 = x2
            h3_2 = h3_1
            h3_1 = x3
        prev_clk = clk
    return res
