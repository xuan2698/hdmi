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
        q = 0x34 if r else d
        out.append({'q': q})
        if 'mid' in row:
            m = row['mid']
            if 'd' in m:
                d = m['d'] & 255
            if 'reset' in m:
                r = m['reset'] & 1
    return out
