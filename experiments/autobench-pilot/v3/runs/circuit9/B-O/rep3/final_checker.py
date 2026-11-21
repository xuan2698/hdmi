def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        clk = row.get('clk', 0)
        a = row.get('a', 0)
        if clk == 1:
            if a == 1:
                q = 4
            else:
                q = (q + 1) % 8
        out.append({'q': q})
        if 'mid' in row:
            m = row['mid']
            if 'a' in m:
                a = m['a']
            if 'clk' in m:
                clk = m['clk']
            if clk == 1:
                if a == 1:
                    q = 4
                else:
                    q = (q + 1) % 8
    return out
