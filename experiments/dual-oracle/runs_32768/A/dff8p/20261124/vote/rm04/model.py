def reference(vectors):
    q = 0
    out = []
    prev_clk = 1
    for v in vectors:
        if 'clk' in v:
            c = v['clk']
            if prev_clk == 1 and c == 0:
                q = 0x34 if v.get('reset', 0) else (v.get('d', 0) & 0xFF)
            prev_clk = c
        else:
            q = 0x34 if v.get('reset', 0) else (v.get('d', 0) & 0xFF)
        out.append({'q': q})
    return out
