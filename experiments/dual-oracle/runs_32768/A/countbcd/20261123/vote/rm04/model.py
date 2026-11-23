def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        if isinstance(row, dict):
            r = row.get("reset", 0)
        elif isinstance(row, (list, tuple)):
            r = row[0]
        else:
            r = row
        if r:
            q = 0
        else:
            o = q & 15
            t = (q >> 4) & 15
            h = (q >> 8) & 15
            th = (q >> 12) & 15
            o += 1
            if o == 10:
                o = 0
                t += 1
                if t == 10:
                    t = 0
                    h += 1
                    if h == 10:
                        h = 0
                        th += 1
                        if th == 10:
                            th = 0
            q = (th << 12) | (h << 8) | (t << 4) | o
        o = q & 15
        t = (q >> 4) & 15
        h = (q >> 8) & 15
        ena = 0
        if o == 9:
            ena |= 1
            if t == 9:
                ena |= 2
                if h == 9:
                    ena |= 4
        out.append({"q": q, "ena": ena})
    return out
