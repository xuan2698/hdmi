def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        if int(row['reset']) & 1:
            q = 0
        else:
            q = int(row['d']) & 0xFF
        out.append({'q': q})
    return out
