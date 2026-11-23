def reference(vectors):
    h = 12
    m = 0
    s = 0
    pm = 0
    out = []
    for row in vectors:
        if isinstance(row, dict):
            r = row.get('reset', 0)
            e = row.get('ena', 0)
        else:
            r = row[0]
            e = row[1] if len(row) > 1 else 0

        if r:
            h = 12
            m = 0
            s = 0
            pm = 0
        elif e:
            s += 1
            if s == 60:
                s = 0
                m += 1
                if m == 60:
                    m = 0
                    h += 1
                    if h == 12:
                        pm ^= 1
                    elif h == 13:
                        h = 1

        out.append({
            "pm": pm,
            "hh": ((h // 10) << 4) | (h % 10),
            "mm": ((m // 10) << 4) | (m % 10),
            "ss": ((s // 10) << 4) | (s % 10),
        })
    return out
