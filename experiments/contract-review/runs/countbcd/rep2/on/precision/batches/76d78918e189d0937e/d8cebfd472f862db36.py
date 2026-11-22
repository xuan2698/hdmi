def reference(vectors):
    q = 0
    outputs = []
    for vin in vectors:
        r = vin.get('reset', 0)
        if r:
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
        ena = 0
        if (q & 15) == 9:
            ena += 1
        if (q & 255) == 0x99:
            ena += 2
        if (q & 4095) == 0x999:
            ena += 4
        outputs.append({'q': q, 'ena': ena})
    return outputs