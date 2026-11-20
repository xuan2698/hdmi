def reference(vectors):
    result = []
    for v in vectors:
        if v["r"] == 1:
            q = 0
        else:
            q = v["d"]
        result.append({"q": q})
    return result
