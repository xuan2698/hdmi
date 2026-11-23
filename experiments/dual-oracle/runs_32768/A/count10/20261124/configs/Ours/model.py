def reference(vectors):
    s = 0
    out = []
    for row in vectors:
        if isinstance(row, dict):
            r = row.get('reset', 0)
        else:
            r = row[0] if len(row) else 0
        if r:
            s = 0
        else:
            s = 0 if s >= 9 else s + 1
        out.append({'q': s})
    return out
