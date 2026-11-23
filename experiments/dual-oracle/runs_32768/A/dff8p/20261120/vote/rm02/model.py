def reference(vectors):
    out = []
    for v in vectors:
        if isinstance(v, dict):
            d = v['d']
            rst = v['reset']
        else:
            d = v[0]
            rst = v[1]
        q = 0x34 if rst else (d & 0xFF)
        out.append({'q': q})
    return out
