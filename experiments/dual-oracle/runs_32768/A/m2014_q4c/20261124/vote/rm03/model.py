def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        q = 0 if v['r'] else v['d']
        out.append({'q': q})
    return out
