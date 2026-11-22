def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        reset = v.get("reset", 0)
        if reset:
            q = 0
        else:
            d0 = q & 15
            d1 = (q >> 4) & 15
            d2 = (q >> 8) & 15
            d3 = (q >> 12) & 15
            if d0 == 9:
                d0 = 0
                if d1 == 9:
                    d1 = 0
                    if d2 == 9:
                        d2 = 0
                        if d3 == 9:
                            d3 = 0
                        else:
                            d3 = d3 + 1
                    else:
                        d2 = d2 + 1
                else:
                    d1 = d1 + 1
            else:
                d0 = d0 + 1
            q = d0 | (d1 << 4) | (d2 << 8) | (d3 << 12)
        d0 = q & 15
        d1 = (q >> 4) & 15
        d2 = (q >> 8) & 15
        ena = 0
        if d0 == 9:
            ena = ena | 1
            if d1 == 9:
                ena = ena | 2
                if d2 == 9:
                    ena = ena | 4
        out.append({"q": q, "ena": ena})
    return out