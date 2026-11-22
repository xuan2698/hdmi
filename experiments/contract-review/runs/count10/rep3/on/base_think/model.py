def reference(vectors):
    q = 0
    cur = 0
    out = []
    for row in vectors:
        if 'reset' in row:
            cur = row['reset']
        if cur:
            q = 0
        else:
            q = (q + 1) % 10
        out.append({'q': q})
        if 'mid' in row:
            m = row['mid']
            if 'reset' in m:
                cur = m['reset']
    return out
