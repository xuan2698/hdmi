def reference(vectors):
    cnt = 31
    res = []
    for i, row in enumerate(vectors):
        edge = 1 if i % 2 == 0 else 0
        rst = 0
        if isinstance(row, dict):
            if 'edge' in row:
                edge = row['edge']
            elif 'clk' in row:
                edge = row['clk']
            if 'reset' in row:
                rst = row['reset']
        elif isinstance(row, (list, tuple)):
            if len(row) == 1:
                rst = row[0]
            elif len(row) >= 2:
                edge = row[0]
                rst = row[1]
        else:
            rst = row
        rst = 1 if rst else 0
        edge = 1 if edge else 0
        if rst:
            cnt = 31
        res.append({
            'cnt_q': cnt,
            'gate_clk_o': 1 if (cnt > 0 and cnt < 14) else 0,
            'release_reset_o': 1 if (cnt < 8) else 0
        })
        if edge and not rst:
            if cnt > 0:
                cnt -= 1
    return res
