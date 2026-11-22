def reference(vectors):
    q = 0
    cur_reset = 0
    out = []
    for row in vectors:
        # Inputs driven before the sampled posedge.
        if "reset" in row:
            cur_reset = row["reset"]

        # R_RESET: synchronous active-high reset has priority.
        if cur_reset == 1:
            q = 0
            # R_ENA_COMB: ena is forced to 0 while reset == 1.
            ena = 0
        else:
            # R_COUNT_BCD: increment packed BCD by 1, wrap 9999 -> 0000.
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

            # R_ENA_COMB: combinational enables from current q.
            ena = 0
            if (q & 15) == 9:
                ena += 1
            if (q & 255) == 0x99:
                ena += 2
            if (q & 4095) == 0x999:
                ena += 4

        out.append({"q": q, "ena": ena})

        # Optional mid changes occur after sampling and carry to next row.
        if "mid" in row:
            mid = row["mid"]
            try:
                if "reset" in mid:
                    cur_reset = mid["reset"]
            except:
                pass
        if "reset_mid" in row:
            cur_reset = row["reset_mid"]
        if "reset__mid" in row:
            cur_reset = row["reset__mid"]
        if "mid_reset" in row:
            cur_reset = row["mid_reset"]
        if "reset@mid" in row:
            cur_reset = row["reset@mid"]

    return out
