def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        r = row.get("reset", 0) if isinstance(row, dict) else row[0]
        if r:
            q = 0
        else:
            q = (q + 1) % 10
        out.append({"q": q})
    return out
