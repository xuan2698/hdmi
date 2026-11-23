def reference(vectors):
    seen = 0
    out = []
    for row in vectors:
        a = row.get('areset', 0)
        x = row.get('x', 0) & 1
        if a:
            seen = 0
            z = 0
        else:
            z = x if seen == 0 else (1 ^ x)
            if x:
                seen = 1
        out.append({'z': z & 1})
    return out
