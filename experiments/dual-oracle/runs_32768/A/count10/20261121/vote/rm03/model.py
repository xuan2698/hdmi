def reference(vectors):
    q = 0
    result = []
    for row in vectors:
        if row["reset"]:
            q = 0
        elif q == 9:
            q = 0
        else:
            q = q + 1
        result.append({"q": q})
    return result
