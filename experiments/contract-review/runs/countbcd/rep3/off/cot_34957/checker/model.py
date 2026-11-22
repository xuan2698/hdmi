def reference(vectors):
    # Contract:
    # - q is a 16-bit BCD counter: q[3:0]=ones, q[7:4]=tens, q[11:8]=hundreds, q[15:12]=thousands.
    # - Synchronous active-high reset forces q=0x0000 at the sampled posedge.
    # - ena is combinational from the settled post-edge q:
    #     ena[0] = ones==9
    #     ena[1] = ones==9 and tens==9
    #     ena[2] = ones==9 and tens==9 and hundreds==9
    # - Mid changes occur after sampling and are carried to the next row.
    # - Power-up state is undefined; assume 0 before first sampled edge.
    q = 0
    out = []
    for row in vectors:
        # Apply any mid changes from the previous row (already stored in row inputs)
        reset = row.get('reset', 0)
        # Synchronous reset at this posedge
        if reset:
            q = 0
        else:
            # Increment BCD counter
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
            q = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones
        # Compute enables from settled post-edge q
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        ena0 = 1 if ones == 9 else 0
        ena1 = 1 if (ones == 9 and tens == 9) else 0
        ena2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        ena = (ena2 << 2) | (ena1 << 1) | ena0
        out.append({'q': q, 'ena': ena})
    return out
