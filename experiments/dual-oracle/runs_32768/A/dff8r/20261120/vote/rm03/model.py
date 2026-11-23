def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        q = 0 if row['reset'] else row['d']
        out.append({'q': q & 0xFF})
    return out
