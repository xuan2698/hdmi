def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        a = row.get('a', 0)
        if row.get('clk', 0) == 1:
            if a == 1:
                q = 0
            else:
                q = (q + 1) % 8
        out.append({'q': q})
    return out
