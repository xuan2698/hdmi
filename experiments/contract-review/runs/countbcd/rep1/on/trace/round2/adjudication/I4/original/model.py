def reference(vectors):
    # RULE reset: synchronous active-high reset; initialize concrete power-up state.
    q = 0
    reset_val = 0
    res = []

    for row in vectors:
        # Drive start-of-row inputs before the sampled posedge.
        if 'reset' in row:
            reset_val = row['reset'] & 1

        # RULE reset: reset has priority over increment at posedge.
        # RULE bcd_increment: BCD add 1 modulo 10000 with carry and wrap 0x9999 -> 0x0000.
        if reset_val == 1:
            q = 0
        else:
            ones = q & 0x0F
            tens = (q >> 4) & 0x0F
            hundreds = (q >> 8) & 0x0F
            thousands = (q >> 12) & 0x0F

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

            q = ((thousands << 12) | (hundreds << 8) | (tens << 4) | ones) & 0xFFFF

        # RULE ena_combinational: compute enables from settled q after posedge.
        ones = q & 0x0F
        tens = (q >> 4) & 0x0F
        hundreds = (q >> 8) & 0x0F

        e0 = 1 if ones == 9 else 0
        e1 = 1 if (tens == 9 and ones == 9) else 0
        e2 = 1 if (hundreds == 9 and tens == 9 and ones == 9) else 0
        ena = e0 | (e1 << 1) | (e2 << 2)

        res.append({'q': q, 'ena': ena})

        # Mid changes occur after sampling, before the other edge, and carry to next row.
        if 'mid' in row:
            mid = row['mid']
            if 'reset' in mid:
                reset_val = mid['reset'] & 1

        # Support direct mid-change key naming if used.
        for k in row:
            if k == 'reset_mid':
                reset_val = row[k] & 1
            elif k == 'mid_reset':
                reset_val = row[k] & 1

    return res
