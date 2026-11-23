def reference(vectors):
    M = 0xFFFFFFFF
    prev = 0
    out = 0
    result = []
    for row in vectors:
        reset = int(row.get("reset", 0)) & 1
        inp = int(row["in"]) & M
        if reset:
            out = 0
        else:
            out = (out | (prev & (~inp) & M)) & M
        prev = inp
        result.append({"out": out})
    return result
