def reference(vectors):
    # R_RESET: synchronous active-high reset forces q to 0
    # R_COUNT_BCD: decrement by 1 on enabled edge, wrapping 0000 to 9999
    # R_ENA_COMB: combinational enables based on current q
    q = 0
    reset = 0
    out = []
    for row in vectors:
        # Each row's values are driven before the sampled edge
        if "reset" in row:
            reset = row["reset"]
        # Sample at posedge
        if reset == 1:
            # R_RESET
            q = 0
        else:
            # R_COUNT_BCD: decrement BCD digit by digit
            ones = q & 15
            tens = (q >> 4) & 15
            hundreds = (q >> 8) & 15
            thousands = (q >> 12) & 15
            if ones == 0:
                ones = 9
                if tens == 0:
                    tens = 9
                    if hundreds == 0:
                        hundreds = 9
                        if thousands == 0:
                            thousands = 9
                        else:
                            thousands -= 1
                    else:
                        hundreds -= 1
                else:
                    tens -= 1
            else:
                ones -= 1
            q = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones
        # R_ENA_COMB: compute enables from post-edge q
        ena = 0
        if (q & 15) == 9:
            ena = ena + 1
        if (q & 255) == 0x99:
            ena = ena + 2
        if (q & 4095) == 0x999:
            ena = ena + 4
        out.append({"q": q, "ena": ena})
        # Optional mid changes occur after sampling, carried to next row
        if "mid" in row:
            mid = row["mid"]
            if "reset" in mid:
                reset = mid["reset"]
    return out
