def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        if isinstance(row, dict):
            reset = row.get('reset', 0)
        elif isinstance(row, (list, tuple)):
            reset = row[0] if row else 0
        else:
            reset = row

        if reset:
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

            q = o | (t << 4) | (h << 8) | (th << 12)

        ena = 0
        if (q & 15) == 9:
            ena |= 1
        if (q & 255) == 0x99:
            ena |= 2
        if (q & 4095) == 0x999:
            ena |= 4

        out.append({'q': q, 'ena': ena})

    return out
