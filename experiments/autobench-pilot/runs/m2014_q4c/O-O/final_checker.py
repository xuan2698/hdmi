def reference(vectors):
    q = None
    out = []
    for v in vectors:
        if v['r'] == 1:
            q = 0
        else:
            q = v['d']
        out.append({'q': q})
    return out
