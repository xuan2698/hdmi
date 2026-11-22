def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        d = v['d']
        reset = v['reset']
        if reset == 1:
            q = 0x34
        else:
            q = d & 0xFF
        out.append({'q': q})
    return out
