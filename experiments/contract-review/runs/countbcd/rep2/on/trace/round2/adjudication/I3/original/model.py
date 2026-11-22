def reference(vectors):
    # R_RESET, R_COUNT_BCD, R_ENA_COMB implemented
    q = 0
    current_reset = 0
    results = []
    for v in vectors:
        # Drive row inputs before sampled posedge
        if "reset" in v:
            current_reset = v["reset"]
        # Sample posedge: synchronous reset or BCD increment
        if current_reset == 1:
            # R_RESET
            q = 0
        else:
            # R_COUNT_BCD: increment 4-digit BCD with wrap at 9999
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
        # R_ENA_COMB: combinational enables from current q
        ena = 0
        if (q & 0xF) == 9:
            ena += 1
        if (q & 0xFF) == 0x99:
            ena += 2
        if (q & 0xFFF) == 0x999:
            ena += 4
        results.append({"q": q, "ena": ena})
        # Process mid changes after sampling, carried to next row
        if "mid" in v:
            mid = v["mid"]
            try:
                if "reset" in mid:
                    current_reset = mid["reset"]
            except TypeError:
                current_reset = mid
        # Support alternative mid key naming
        if "reset_mid" in v:
            current_reset = v["reset_mid"]
        if "mid_reset" in v:
            current_reset = v["mid_reset"]
    return results
