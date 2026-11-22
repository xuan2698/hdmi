def reference(vectors):
    q_count = 0
    result = []
    for row in vectors:
        if "reset" in row:
            reset = row["reset"]
        else:
            reset = 0
        # sync_reset: synchronous active-high reset clears q to 0, overrides increment
        if reset:
            q_count = 0
        else:
            # bcd_increment: increment as 4-digit BCD modulo 10000
            q_count += 1
            if q_count >= 10000:
                q_count = 0
        # convert decimal count to packed BCD 16-bit q
        ones = q_count % 10
        tens = (q_count // 10) % 10
        hundreds = (q_count // 100) % 10
        thousands = (q_count // 1000) % 10
        q = ones | (tens << 4) | (hundreds << 8) | (thousands << 12)
        # upper_digit_enables: combinational from current q digits
        bit0 = 1 if ones == 9 else 0
        bit1 = 1 if (ones == 9 and tens == 9) else 0
        bit2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        ena = bit0 + 2 * bit1 + 4 * bit2
        result.append({"q": q, "ena": ena})
    return result
