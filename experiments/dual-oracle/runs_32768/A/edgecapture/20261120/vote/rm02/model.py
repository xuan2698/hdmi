def reference(vectors):
    out = 0
    prev = 0
    prev_clk = 0
    has_clk = any('clk' in r for r in vectors) if vectors else False
    use_edges = False
    if has_clk:
        vals = [int(r['clk']) & 1 for r in vectors if 'clk' in r]
        use_edges = bool(vals) and min(vals) != max(vals)
    result = []
    for row in vectors:
        edge = True
        if use_edges:
            c = int(row.get('clk', 0)) & 1
            edge = prev_clk == 0 and c == 1
            prev_clk = c
        if edge:
            rst = int(row.get('reset', 0)) & 1
            x = int(row.get('in', 0)) & 0xffffffff
            if rst:
                out = 0
            else:
                out = (out | (prev & ((~x) & 0xffffffff))) & 0xffffffff
            prev = x
        result.append({'out': out & 0xffffffff})
    return result
