def reference(vectors):
    # Initial registered state: power-up unspecified, choose concrete 0.
    q = 0
    reset_hold = 0
    result = []
    for row in vectors:
        # Determine reset value at this sampled posedge.
        reset_edge = reset_hold
        if 'reset' in row:
            reset_edge = row['reset'] & 1
            reset_hold = reset_edge

        # Rule reset: synchronous active-high reset asserts but leaves q/ena unchanged.
        if reset_edge == 0:
            # Rule bcd_increment: BCD add 1 modulo 10000.
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF
            if ones < 9:
                ones += 1
            else:
                ones = 0
                if tens < 9:
                    tens += 1
                else:
                    tens = 0
                    if hundreds < 9:
                        hundreds += 1
                    else:
                        hundreds = 0
                        if thousands < 9:
                            thousands += 1
                        else:
                            thousands = 0
            q = (ones | (tens << 4) | (hundreds << 8) | (thousands << 12)) & 0xFFFF
        # else: reset asserted, hold q unchanged

        # Rule ena_combinational: compute enables from registered q.
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        ena0 = 1 if ones == 9 else 0
        ena1 = 1 if (tens == 9 and ones == 9) else 0
        ena2 = 1 if (hundreds == 9 and tens == 9 and ones == 9) else 0
        ena = ena0 | (ena1 << 1) | (ena2 << 2)

        result.append({"q": q & 0xFFFF, "ena": ena & 0x7})

        # Process optional mid changes after sampling; carry to next row.
        if 'mid' in row:
            mid = row['mid']
            if 'reset' in mid:
                reset_hold = mid['reset'] & 1
        for k in row:
            if k != 'mid' and 'mid' in k and 'reset' in k:
                reset_hold = row[k] & 1
    return result
