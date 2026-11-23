def reference(vectors):
    q = 4
    pa = 1
    out = []
    for v in vectors:
        a = v["a"]
        if a:
            q = 4
        elif pa == 0:
            q = 0 if q == 6 else q + 1
        else:
            q = 4
        out.append({"q": q})
        pa = a
    return out
