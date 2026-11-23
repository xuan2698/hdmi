def reference(vectors):
    cnt = 31
    out = []
    for row in vectors:
        if isinstance(row, dict):
            reset = row.get('reset', 0)
            edge = row.get('edge', '')
        else:
            reset = 0
            edge = ''
            if isinstance(row, (list, tuple)):
                for x in row:
                    if isinstance(x, str) and ('pos' in x.lower() or 'neg' in x.lower()):
                        edge = x
                    else:
                        reset = x
            else:
                reset = row
        if isinstance(reset, str):
            reset = 1 if reset.lower() in ('1', 'true', 'high') else 0
        else:
            reset = int(reset) & 1
        is_pos = False
        if isinstance(edge, str):
            e = edge.lower()
            if 'pos' in e or e == '1' or e.startswith('p'):
                is_pos = True
        elif isinstance(edge, (int, bool)):
            is_pos = (int(edge) & 1) == 1
        if reset:
            cnt = 31
        gate = 1 if 0 < cnt < 14 else 0
        rel = 1 if cnt < 8 else 0
        out.append({'cnt_q': cnt, 'gate_clk_o': gate, 'release_reset_o': rel})
        if is_pos:
            if reset:
                cnt = 31
            elif cnt > 0:
                cnt -= 1
    return out
