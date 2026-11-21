def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        if row.get('reset', 0):
            q = 0
        else:
            q = (q + 1) % 10
        out.append({'q': q})
        if 'mid' in row:
            m = row['mid']
            if m.get('reset', 0):
                q = 0
    return out
