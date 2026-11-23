def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        d = row["d"]
        reset = row["reset"]
        if reset:
            q = 0x34
        else:
            q = d & 0xFF
        out.append({"q": q})
    return out
