def reference(vectors):
    s = 0
    out = []
    for v in vectors:
        a = v["a"]
        b = v["b"]
        s = (a & b) if s == 0 else (a | b)
        out.append({"q": s ^ a ^ b, "state": s})
    return out
