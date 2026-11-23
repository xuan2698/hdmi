def reference(vectors):
    d = 0
    r = 0
    q = 0
    out = []
    for row in vectors:
        if 'd' in row:
            d = row['d'] & 255
        if 'reset' in row:
            r = row['reset'] & 1
        q = 0 if r else (d & 255)
        out.append({'q': q})
        if 'mid' in row and isinstance(row['mid'], dict):
            m = row['mid']
            if 'd' in m:
                d = m['d'] & 255
            if 'reset' in m:
                r = m['reset'] & 1
    return out
