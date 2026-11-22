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
                ena |= 4
            if ones == 9 and tens == 9 and hundreds == 9:
                ena |= 8
            n_ones = (ones + 1) % 10
            n_tens = tens
            n_hundreds = hundreds
            n_thousands = thousands
            if ones == 9:
                n_tens = (tens + 1) % 10
            if ones == 9 and tens == 9:
                n_hundreds = (hundreds + 1) % 10
            if ones == 9 and tens == 9 and hundreds == 9:
                n_thousands = (thousands + 1) % 10
            q = n_ones | (n_tens << 4) | (n_hundreds << 8) | (n_thousands << 12)
        out.append({'q': q, 'ena': ena})
    return out
