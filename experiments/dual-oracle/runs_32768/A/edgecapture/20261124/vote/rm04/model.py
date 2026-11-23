def reference(vectors):
    prev = 0
    out = 0
    result = []
    for row in vectors:
        reset = row["reset"] & 1
        cur = row["in"] & 0xFFFFFFFF
        if reset:
            out = 0
        else:
            out = (out | (prev & (cur ^ 0xFFFFFFFF))) & 0xFFFFFFFF
        prev = cur
        result.append({"out": out})
    return result
