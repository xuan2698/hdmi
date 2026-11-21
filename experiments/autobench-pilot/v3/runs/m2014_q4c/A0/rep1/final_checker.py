def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        d = row.get('d', 0)
        r = row.get('r', 0)
        if r:
            q = 0
        else:
            q = d
        out.append({'q': q})
        if 'mid' in row:
            m = row['mid']
            if m.get('r', 0):
                q = 0
            elif 'd' in m:
                q = m['d']
    return out
