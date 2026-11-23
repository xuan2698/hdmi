def reference(vectors):
    out = []
    for row in vectors:
        q = 0x34 if row.get('reset', 0) else (row.get('d', 0) & 0xFF)
        out.append({'q': q & 0xFF})
    return out
