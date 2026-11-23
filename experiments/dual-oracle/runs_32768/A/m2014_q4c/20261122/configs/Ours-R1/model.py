def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        d = row["d"]
        r = row["r"]
        if r:
            q = 0
        else:
            q = d
        out.append({"q": q})
    return out
