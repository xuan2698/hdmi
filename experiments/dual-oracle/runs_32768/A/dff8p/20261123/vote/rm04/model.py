def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        if row.get('reset', 0):
            q = 0x34
        else:
            q = row.get('d', 0) & 0xFF
        out.append({'q': q})
    return out
