def reference(vectors):
    prev = [None] * 32
    out = [None] * 32
    result = []
    for row in vectors:
        rst = row.get("reset", 0)
        inv = row.get("in", 0)
        in_bits = [(inv >> i) & 1 for i in range(32)]
        if rst:
            out = [0] * 32
            prev = in_bits
        else:
            new_out = [None] * 32
            for i in range(32):
                p = prev[i]
                ib = in_bits[i]
                if p is None:
                    det = None
                else:
                    det = p & (1 - ib)
                o = out[i]
                if o is None:
                    if det == 1:
                        new_out[i] = 1
                    else:
                        new_out[i] = None
                else:
                    if o == 1:
                        new_out[i] = 1
                    else:
                        if det is None:
                            new_out[i] = None
                        else:
                            new_out[i] = det
            out = new_out
            prev = in_bits

        if all(x is not None for x in out):
            val = 0
            for i in range(32):
                if out[i]:
                    val |= (1 << i)
            result.append({"out": val})
        else:
            result.append({"out": None})
    return result
