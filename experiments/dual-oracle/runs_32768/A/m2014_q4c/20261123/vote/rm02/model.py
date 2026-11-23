def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        if isinstance(row, dict):
            d = row.get('d', 0)
            r = row.get('r', 0)
        else:
            d = row[0]
            r = row[1]
        q = 0 if r else (d & 1)
        out.append({'q': q})
    return out
