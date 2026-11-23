def reference(vectors):
    cnt = 31
    out = []
    expect_pos = True
    for row in vectors:
        reset_val = 0
        edge_pos = expect_pos
        if isinstance(row, dict):
            if 'reset' in row:
                reset_val = int(row['reset']) & 1
            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    le = e.lower()
                    if 'pos' in le:
                        edge_pos = True
                    elif 'neg' in le:
                        edge_pos = False
                elif isinstance(e, (int, bool)):
                    edge_pos = (e == 1)
            elif 'clk' in row:
                c = row['clk']
                if isinstance(c, str):
                    lc = c.lower()
                    if 'pos' in lc or c == '1':
                        edge_pos = True
                    elif 'neg' in lc or c == '0':
                        edge_pos = False
                elif isinstance(c, (int, bool)):
                    edge_pos = (c == 1)

        if reset_val == 1:
            cnt = 31

        q = cnt & 31
        gate = 1 if (q > 0 and q < 14) else 0
        rel = 1 if q < 8 else 0
        out.append({'cnt_q': q, 'gate_clk_o': gate, 'release_reset_o': rel})

        if edge_pos:
            if reset_val == 1:
                cnt = 31
            elif cnt > 0:
                cnt -= 1

        expect_pos = not edge_pos

    return out
