def reference(vectors):
    q = 0x34
    out = []
    for row in vectors:
        if row['reset']:
            q = 0x34
        else:
            q = row['d'] & 0xFF
        out.append({'q': q})
    return out
