def reference(vectors):
    seen = 0
    out = []
    for row in vectors:
        areset = row.get('areset', 0) & 1
        x = row.get('x', 0) & 1
        if areset:
            seen = 0
            z = 0
        else:
            z = (1 - x) if seen else x
            if x:
                seen = 1
        out.append({'z': z & 1})
    return out
