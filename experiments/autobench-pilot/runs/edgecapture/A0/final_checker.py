def reference(vectors):
    out = [None] * 32
    prev = [None] * 32
    result = []
    for row in vectors:
        reset = row["reset"]
        inv = row["in"]
        for i in range(32):
            bit = (inv >> i) & 1
            if reset:
                nxt = 0
            else:
                fall = prev[i] if bit == 0 else 0
                if out[i] == 1 or fall == 1:
                    nxt = 1
                elif out[i] == 0 and fall == 0:
                    nxt = 0
                else:
                    nxt = None
            prev[i] = bit
            out[i] = nxt
        value = 0
        known = True
        for i in range(32):
            if out[i] is None:
                known = False
                break
            if out[i]:
                value |= 1 << i
        result.append({"out": value if known else None})
    return result
