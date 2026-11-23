def reference(vectors):
    q = 0x34
    prev_clk = 1
    out = []
    for r in vectors:
        if 'clk' in r:
            clk = r['clk']
            if prev_clk == 1 and clk == 0:
                if r.get('reset', 0):
                    q = 0x34
                else:
                    q = r.get('d', 0) & 0xFF
            prev_clk = clk
        else:
            if r.get('reset', 0):
                q = 0x34
            else:
                q = r.get('d', 0) & 0xFF
        out.append({'q': q & 0xFF})
    return out
