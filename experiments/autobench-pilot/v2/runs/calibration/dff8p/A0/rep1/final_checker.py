def reference(vectors):
    q = None
    out = []
    for row in vectors:
        d = row['d']
        reset = row['reset']
        if reset:
            q = 0x34
        else:
            if q is None:
                q = d
            else:
                q = d
        out.append({'q': q & 0xFF})
    return out
