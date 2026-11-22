def reference(vectors):
    q = 0
    current_reset = 0
    result = []
    for row in vectors:
        # Apply row inputs before sampled edge
        if "reset" in row:
            current_reset = row["reset"]
        # Sampled posedge
        if current_reset == 1:
            # R_RESET: synchronous active-high reset forces q=0
            q_next = 0
        else:
            # R_COUNT_BCD: increment packed BCD counter modulo 10000
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF
            if ones == 9:
                ones = 0
                if tens == 9:
                    tens = 0
                    if hundreds == 9:
                        hundreds = 0
                        if thousands == 9:
                            thousands = 0
                        else:
                            thousands += 1
                    else:
                        hundreds += 1
                else:
                    tens += 1
            else:
                ones += 1
            q_next = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones
        q = q_next
        # R_ENA_COMB: combinational enable from current q
        ena0 = 1 if (q & 0xF) == 9 else 0
        ena1 = 1 if (q & 0xFF) == 0x99 else 0
        ena2 = 1 if (q & 0xFFF) == 0x999 else 0
        ena = ena0 + (ena1 << 1) + (ena2 << 2)
        result.append({"q": q, "ena": ena})
        # Process mid changes after sampling
        if "mid" in row:
            mid = row["mid"]
            if "reset" in mid:
                current_reset = mid["reset"]
    return result
