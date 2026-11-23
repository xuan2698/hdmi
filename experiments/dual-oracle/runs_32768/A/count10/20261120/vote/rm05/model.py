def reference(vectors):
    s = 0
    out = []
    for v in vectors:
        if v['reset']:
            s = 0
        else:
            s = 0 if s == 9 else s + 1
        out.append({'q': s})
    return out
