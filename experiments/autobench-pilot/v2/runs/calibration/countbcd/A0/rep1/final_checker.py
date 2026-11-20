def reference(vectors):
    out = []
    q = 0
    for v in vectors:
        reset = v.get('reset', 0)
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
            q = ones | (tens << 4) | (hundreds << 8) | (thousands << 12)
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        thousands = (q >> 12) & 0xF
        ena = 0
        if ones == 9:
            ena |= 1
        if tens == 9 and ones == 9:
            ena |= 2
        if hundreds == 9 and tens == 9 and ones == 9:
            ena |= 4
        out.append({'ena': ena, 'q': q})
    return out
