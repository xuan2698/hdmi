def reference(vectors):
    q = None
    out = []
    for v in vectors:
        clk = v.get('clk')
        a = v.get('a')
        if clk == 1:
            if q is None:
                q = 4
            else:
                if a == 1:
                    q = 4
                else:
                    q = (q + 1) % 8
        out.append({'q': q})
    return out
