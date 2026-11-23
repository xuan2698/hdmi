def reference(vectors):
    prev = 0
    out = 0
    result = []
    for row in vectors:
        reset = row.get("reset", 0)
        cur = row.get("in", 0) & 0xFFFFFFFF
        if reset:
            out = 0
        else:
            out = (out | (prev & (~cur))) & 0xFFFFFFFF
        prev = cur
        result.append({"out": out})
    return result
