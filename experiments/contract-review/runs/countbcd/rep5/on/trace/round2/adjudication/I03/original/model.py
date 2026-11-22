def reference(vectors):
    # sync_reset: synchronous active-high reset clears q to 0
    # bcd_increment: increment 4-digit BCD counter modulo 10000
    # upper_digit_enables: combinational enables for upper digits
    d0 = 0
    d1 = 0
    d2 = 0
    d3 = 0
    out = []
    for row in vectors:
        reset = row["reset"]
        if reset == 1:
            d0 = 0
            d1 = 0
            d2 = 0
            d3 = 0
        else:
            d0 = d0 + 1
            if d0 == 10:
                d0 = 0
                d1 = d1 + 1
                if d1 == 10:
                    d1 = 0
                    d2 = d2 + 1
                    if d2 == 10:
                        d2 = 0
                        d3 = d3 + 1
                        if d3 == 10:
                            d3 = 0
        q = d0 + (d1 << 4) + (d2 << 8) + (d3 << 12)
        ena = 0
        if d0 == 9:
            ena = ena + 1
        if d0 == 9 and d1 == 9:
            ena = ena + 2
        if d0 == 9 and d1 == 9 and d2 == 9:
            ena = ena + 4
        out.append({"q": q, "ena": ena})
    return out
