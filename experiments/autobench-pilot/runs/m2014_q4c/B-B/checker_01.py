def reference(vectors):
    out = []
    for v in vectors:
        if v["r"]:
            q = 0
        else:
            q = v["d"]
        out.append({"q": q})
    return out
