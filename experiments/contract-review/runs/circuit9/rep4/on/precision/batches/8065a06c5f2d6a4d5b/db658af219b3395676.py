def reference(vectors):
    has_clk = False
    clk_changes = False
    last_clk = None
    for v in vectors:
        if 'clk' in v:
            has_clk = True
            c = v['clk']
            if last_clk is not None and c != last_clk:
                clk_changes = True
            last_clk = c
    q = 0
    prev_a = 0
    out = []
    if has_clk and clk_changes:
        prev_clk = 0
        for v in vectors:
            clk = v.get('clk', 0)
            if clk == 1 and prev_clk == 0:
                a = v.get('a', 0)
                if a == 1:
                    q = 4
                else:
                    if prev_a == 0:
                        q = (q + 1) % 7
                prev_a = a
            prev_clk = clk
            out.append({'q': q})
    else:
        for v in vectors:
            a = v['a']
            if a == 1:
                q = 4
            else:
                if prev_a == 0:
                    q = (q + 1) % 7
            prev_a = a
            out.append({'q': q})
    return out