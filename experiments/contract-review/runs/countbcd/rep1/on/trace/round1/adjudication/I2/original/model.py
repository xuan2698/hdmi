def reference(vectors):
    q = 0
    cur_reset = 0
    result = []
    for row in vectors:
        # Apply primary inputs before posedge
        if "reset" in row:
            cur_reset = row["reset"]
        # Synchronous active-high reset has priority over increment
        if cur_reset == 1:
            q = 0
        else:
            # BCD increment modulo 10000
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF
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
        # Combinational enable from updated q
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        ena = 0
        if ones == 9:
            ena = ena | 1
            if tens == 9:
                ena = ena | 2
                if hundreds == 9:
                    ena = ena | 4
        result.append({"q": q, "ena": ena})
        # Apply mid changes after sampling (carried to next row)
        if "mid" in row:
            mid = row["mid"]
            try:
                if "reset" in mid:
                    cur_reset = mid["reset"]
            except:
                try:
                    cur_reset = mid
                except:
                    pass
        if "reset_mid" in row:
            cur_reset = row["reset_mid"]
        if "mid_reset" in row:
            cur_reset = row["mid_reset"]
    return result
