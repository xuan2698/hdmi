def reference(vectors):
    # Rule reset: synchronous active-high reset has priority over increment.
    # Rule bcd_increment: BCD add 1 modulo 10000.
    # Rule ena_combinational: combinational enable from q after settle.
    q = 0
    cur_reset = 0
    out = []
    for row in vectors:
        mid_reset = None
        mid = None
        for k, v in row.items():
            if k == "reset":
                cur_reset = v
            elif k == "mid" or k == "__mid__" or k == "mid_changes":
                mid = v
            elif "reset" in k and "mid" in k:
                mid_reset = v

        # Sample posedge clk after row inputs are driven.
        if cur_reset == 1:
            # reset rule
            q = 0
        else:
            # bcd_increment rule
            ones = q & 15
            tens = (q >> 4) & 15
            hundreds = (q >> 8) & 15
            thousands = (q >> 12) & 15
            ones = ones + 1
            if ones == 10:
                ones = 0
                tens = tens + 1
                if tens == 10:
                    tens = 0
                    hundreds = hundreds + 1
                    if hundreds == 10:
                        hundreds = 0
                        thousands = thousands + 1
                        if thousands == 10:
                            thousands = 0
            q = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones

        # ena_combinational rule
        ones = q & 15
        tens = (q >> 4) & 15
        hundreds = (q >> 8) & 15
        en0 = 1 if ones == 9 else 0
        en1 = 1 if tens == 9 and ones == 9 else 0
        en2 = 1 if hundreds == 9 and tens == 9 and ones == 9 else 0
        ena = en0 | (en1 << 1) | (en2 << 2)

        out.append({"q": q, "ena": ena})

        # Mid changes occur after sampling and are carried to the start of the next row.
        if mid is not None:
            if "reset" in mid:
                cur_reset = mid["reset"]
        if mid_reset is not None:
            cur_reset = mid_reset

    return out
