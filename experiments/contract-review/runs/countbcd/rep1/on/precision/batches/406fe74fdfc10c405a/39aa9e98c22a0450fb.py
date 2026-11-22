def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        r = v.get('reset', 0)
        if r == 1:
            q = 0
        else:
            ones = q & 15
            tens = (q >> 4) & 15
            hundreds = (q >> 8) & 15
            thousands = (q >> 12) & 15
            ones += 1
            carry = 0
            if ones > 9:
                ones = 0
                carry = 1
            if carry:
                tens += 1
                if tens > 9:
                    tens = 0
                    carry = 1
                else:
                    carry = 0
            if carry:
                hundreds += 1
                if hundreds > 9:
                    hundreds = 0
                    carry = 1
                else:
                    carry = 0
            if carry:
                thousands += 1
                if thousands > 9:
                    thousands = 0
                else:
                    carry = 0
            q = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones
        ones = q & 15
        tens = (q >> 4) & 15
        hundreds = (q >> 8) & 15
        ena = 0
        if ones == 9:
            ena |= 1
        if tens == 9 and ones == 9:
            ena |= 2
        if hundreds == 9 and tens == 9 and ones == 9:
            ena |= 4
        out.append({'q': q & 65535, 'ena': ena & 7})
    return out