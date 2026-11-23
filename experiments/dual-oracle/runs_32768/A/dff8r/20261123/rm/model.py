def reference(vectors):
    out = []
    for row in vectors:
        if isinstance(row, dict):
            d = row.get('d', 0)
            reset = row.get('reset', 0)
        else:
            d = row[0] if len(row) > 0 else 0
            reset = row[1] if len(row) > 1 else 0
        out.append({'q': 0 if reset else (d & 0xFF)})
    return out
