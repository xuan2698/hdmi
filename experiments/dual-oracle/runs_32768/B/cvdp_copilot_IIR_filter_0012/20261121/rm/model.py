def reference(vectors):
    out_1 = out_2 = out_3 = 0
    prev_clk = 0
    res = []
    for i, row in enumerate(vectors):
        clk = row.get('clk', 1 if i % 2 == 0 else 0)
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                clk = 1 if 'pos' in e.lower() else 0
            else:
                clk = e
        reset = row.get('reset', 0)
        if reset == 1:
            out_1 = out_2 = out_3 = 0
        cur_1, cur_2, cur_3 = (0, 0, 0) if reset == 1 else (out_1, out_2, out_3)
        res.append({
            'out_1': cur_1 & 0xFFFF,
            'out_2': cur_2 & 0xFFFF,
            'out_3': cur_3 & 0xFFFF
        })
        if reset == 0 and clk == 1 and prev_clk == 0:
            out_1 = row.get('in_1', 0) & 0xFFFF
            out_2 = row.get('in_2', 0) & 0xFFFF
            out_3 = row.get('in_3', 0) & 0xFFFF
        prev_clk = clk
    return res
