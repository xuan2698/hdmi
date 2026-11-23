def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        if row['reset']:
            q = 0
        else:
            q = row['d'] & 255
        out.append({'q': q})
    return out
