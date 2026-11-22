def reference(vectors):
    # R_RESET, R_COUNT_BCD, R_ENA_COMB implemented below
    q = 0
    current_reset = 0
    result = []
    for row in vectors:
        if "reset" in row:
            current_reset = row["reset"]
        reset_val = current_reset

        # R_RESET: synchronous active-high reset forces q to 0
        if reset_val:
            q = 0
        else:
            # R_COUNT_BCD: 4-digit BCD increment modulo 10000
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

        # R_ENA_COMB: candidate mapping
        # ena[2]=tens enable (ones==9), ena[1]=hundreds enable (lower2==99), ena[0]=thousands enable (lower3==999)
        ones = q & 15
        tens = (q >> 4) & 15
        hundreds = (q >> 8) & 15
        bit2 = 1 if ones == 9 else 0
        bit1 = 1 if (ones == 9 and tens == 9) else 0
        bit0 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        ena = (bit2 << 2) | (bit1 << 1) | bit0

        result.append({"q": q, "ena": ena})

        # Process optional mid changes after sampling (carried to next row)
        mid_reset = None
        if "mid" in row:
            try:
                mid_dict = row["mid"]
                if "reset" in mid_dict:
                    mid_reset = mid_dict["reset"]
            except:
                pass
        for key in row:
            if key == "mid":
                continue
            if "mid" in key and "reset" in key:
                mid_reset = row[key]
        if mid_reset is not None:
            current_reset = mid_reset

    return result
