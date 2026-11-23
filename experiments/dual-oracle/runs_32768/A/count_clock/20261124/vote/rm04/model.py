def reference(vectors):
    h = 12
    m = 0
    s = 0
    pm = 0
    outputs = []

    for row in vectors:
        reset = int(row.get('reset', 0))
        ena = int(row.get('ena', 0))

        if reset:
            h = 12
            m = 0
            s = 0
            pm = 0
        elif ena:
            s += 1
            if s == 60:
                s = 0
                m += 1
                if m == 60:
                    m = 0
                    if h == 12:
                        h = 1
                    else:
                        h += 1
                        if h == 12:
                            pm ^= 1

        hh = ((h // 10) << 4) | (h % 10)
        mm = ((m // 10) << 4) | (m % 10)
        ss = ((s // 10) << 4) | (s % 10)

        outputs.append({
            'pm': pm,
            'hh': hh,
            'mm': mm,
            'ss': ss
        })

    return outputs
