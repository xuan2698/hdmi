def reference(vectors):
    cnt = 31
    out = []
    alt_pos = True
    for row in vectors:
        reset_val = 0
        edge_pos = alt_pos
        if isinstance(row, dict):
            if 'reset' in row:
                reset_val = int(row['reset'])
            if 'clk' in row:
                v = row['clk']
                if isinstance(v, str):
                    lv = v.lower()
                    if 'pos' in lv or v == '1':
                        edge_pos = True
                    elif 'neg' in lv or v == '0':
                        edge_pos = False
                elif isinstance(v, (int, bool)):
                    edge_pos = (v == 1)
            elif 'edge' in row:
                v = row['edge']
                if isinstance(v, str):
                    lv = v.lower()
                    if 'pos' in lv:
                        edge_pos = True
                    elif 'neg' in lv:
                        edge_pos = False
                elif isinstance(v, (int, bool)):
                    edge_pos = (v == 1)
        if reset_val == 1:
            cnt = 31
        c = cnt & 0x1F
        gate = 1 if (c > 0 and c < 14) else 0
        rel = 1 if (c < 8) else 0
        out.append({'cnt_q': c, 'gate_clk_o': gate, 'release_reset_o': rel})
        if edge_pos:
            if reset_val == 1:
                cnt = 31
            else:
                if cnt > 0:
                    cnt = cnt - 1
        alt_pos = not edge_pos
    return out
