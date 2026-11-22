def reference(vectors):
    q = 0  # initial state; power-up unspecified but choose concrete 0
    out = []
    for row in vectors:
        reset = int(row.get('reset', 0)) & 1
        # sync_reset: synchronous active-high reset clears q to 0, priority over increment.
        if reset == 1:
            q = 0
        else:
            # bcd_increment: increment 4-digit BCD modulo 10000.
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
            q = ((thousands & 0xF) << 12) | ((hundreds & 0xF) << 8) | ((tens & 0xF) << 4) | (ones & 0xF)
            q &= 0xFFFF
        # upper_digit_enables: combinational from current q.
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        b0 = 1 if ones == 9 else 0
        b1 = 1 if (ones == 9 and tens == 9) else 0
        b2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        ena = (b0 + (b1 << 1) + (b2 << 2)) & 0x7
        out.append({"q": q & 0xFFFF, "ena": ena})
    return out
