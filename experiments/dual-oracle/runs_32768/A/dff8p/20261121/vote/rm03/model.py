def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        if isinstance(row, dict):
            d = row['d']
            rst = row['reset']
        else:
            d = row[0]
            rst = row[1]
        if rst:
            q = 0x34
        else:
            q = d & 0xFF
        out.append({'q': q})
    return out
