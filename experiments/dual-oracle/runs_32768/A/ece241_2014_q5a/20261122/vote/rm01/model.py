def reference(vectors):
    seen = False
    out = []
    for row in vectors:
        if row.get('areset', 0):
            seen = False
            z = 0
        else:
            x = int(row.get('x', 0)) & 1
            if not seen:
                z = x
                if x:
                    seen = True
            else:
                z = 1 - x
        out.append({'z': z})
    return out
