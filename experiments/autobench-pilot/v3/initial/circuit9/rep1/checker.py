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
        mid = row.get('mid')
        if mid:
            if 'a' in mid:
                a = mid['a']
            if 'clk' in mid:
                clk = mid['clk']
            if clk == 1:
                if a == 1:
                    q = 4
                else:
                    q = (q + 1) % 8
            out[-1]['q'] = q
    return out
