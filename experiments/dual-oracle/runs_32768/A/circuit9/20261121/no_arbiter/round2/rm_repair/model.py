def reference(vectors):
    q = 4
    result = []
    for row in vectors:
        if row["a"]:
            q = 4
        elif q == 6:
            q = 0
        else:
            q = (q + 1) & 7
        result.append({"q": q})
    return result
