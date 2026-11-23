def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        d = row['d']
        r = row['reset']
        q = 0 if (r & 1) else (d & 0xFF)
        out.append({'q': q})
    return out
