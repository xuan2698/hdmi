def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        a = row.get('a', 0)
        if row.get('clk', 0) == 1:
            q = (q + 1) % 8 if a == 0 else q
        out.append({'q': q})
    return out
