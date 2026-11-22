def reference(vectors):
    q = 0
    result = []
    for v in vectors:
        if v['reset']:
            q = 0
        else:
            ones = q & 15
            tens = (q >> 4) & 15
            hundreds = (q >> 8) & 15
            thousands = (q >> 12) & 15
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
        ones = q & 15
        tens = (q >> 4) & 15
        hundreds = (q >> 8) & 15
        bit0 = 1 if ones == 9 else 0
        bit1 = 1 if (ones == 9 and tens == 9) else 0
        bit2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        ena = bit0 | (bit1 << 1) | (bit2 << 2)
        result.append({'q': q & 65535, 'ena': ena & 7})
    return result