def reference(vectors):
    q = 0
    result = []
    for row in vectors:
        reset = row['reset'] if isinstance(row, dict) else row
        if reset:
            q = 0
        else:
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF
            ones += 1
            carry = 0
            if ones == 10:
                ones = 0
                carry = 1
            if carry:
                tens += 1
                carry = 0
                if tens == 10:
                    tens = 0
                    carry = 1
            if carry:
                hundreds += 1
                carry = 0
                if hundreds == 10:
                    hundreds = 0
                    carry = 1
            if carry:
                thousands += 1
                if thousands == 10:
                    thousands = 0
            q = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        e0 = 1 if ones == 9 else 0
        e1 = 1 if (ones == 9 and tens == 9) else 0
        e2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        ena = e0 | (e1 << 1) | (e2 << 2)
        result.append({'ena': ena, 'q': q})
    return result
