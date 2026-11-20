def reference(vectors):
    prev = [None] * 32
    out = [None] * 32
    result = []
    for row in vectors:
        rst = row.get("reset", 0)
        inv = row.get("in", 0)
        cur = [(inv >> i) & 1 for i in range(32)]
        if rst:
            out = [0] * 32
            prev = cur
        else:
            nxt = [None] * 32
            for i in range(32):
                if out[i] == 1:
                    nxt[i] = 1
                else:
                    p = prev[i]
                    c = cur[i]
                    if p is None:
                        d = None
                    else:
                        d = p & (1 - c)
                    if d == 1:
                        nxt[i] = 1
                    elif out[i] == 0 and d == 0:
                        nxt[i] = 0
                    else:
                        nxt[i] = None
            out = nxt
            prev = cur
        known = True
        val = 0
        for i in range(32):
            if out[i] is None:
                known = False
                break
            if out[i]:
                val |= (1 << i)
        if known:
            result.append({"out": val})
        else:
            result.append({"out": None})
    return result
