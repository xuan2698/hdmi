def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        reset = v['reset']
        if reset:
            q = 0
        else:
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF
            ones += 1
            if ones == 10:
                ones = 0
                tens += 1
                if tens == 10:
                    tens = 0
                    hundreds += 1
                    if hundreds == 10:
                        hundreds = 0
                        thousands += 1
                        if thousands == 10:
                            thousands = 0
            q = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones

        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        e0 = 1 if ones == 9 else 0
        e1 = 1 if ones == 9 and tens == 9 else 0
        e2 = 1 if ones == 9 and tens == 9 and hundreds == 9 else 0
        ena = (e2 << 2) | (e1 << 1) | e0
        out.append({'q': q, 'ena': ena})
    return out
