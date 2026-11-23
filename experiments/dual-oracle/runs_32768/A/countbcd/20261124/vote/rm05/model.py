def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        reset = row['reset'] if isinstance(row, dict) else row[0]
        if reset:
            q = 0
        else:
            ones = q & 15
            tens = (q >> 4) & 15
            hundreds = (q >> 8) & 15
            thousands = (q >> 12) & 15
            if ones == 9:
                ones = 0
                if tens == 9:
                    tens = 0
                    if hundreds == 9:
                        hundreds = 0
                        if thousands == 9:
                            thousands = 0
                        else:
                            thousands += 1
                    else:
                        hundreds += 1
                else:
                    tens += 1
            else:
                ones += 1
            q = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones
        ones = q & 15
        tens = (q >> 4) & 15
        hundreds = (q >> 8) & 15
        ena = (1 if ones == 9 else 0)
        ena |= ((1 if ones == 9 and tens == 9 else 0) << 1)
        ena |= ((1 if ones == 9 and tens == 9 and hundreds == 9 else 0) << 2)
        out.append({'ena': ena, 'q': q})
    return out
