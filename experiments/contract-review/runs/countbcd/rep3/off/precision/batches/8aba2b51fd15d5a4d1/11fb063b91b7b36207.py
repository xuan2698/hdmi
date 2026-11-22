def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        reset = v.get('reset', 0)
        if reset:
            q = 0
            ena = 0
        else:
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF
            ena = 0
            if ones == 9:
                ena |= 1
            if ones == 9 and tens == 9:
                ena |= 2
            if ones == 9 and tens == 9 and hundreds == 9:
                ena |= 4
            if ones == 9:
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
            else:
                ones += 1
            q = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones
        out.append({'q': q, 'ena': ena})
    return out
