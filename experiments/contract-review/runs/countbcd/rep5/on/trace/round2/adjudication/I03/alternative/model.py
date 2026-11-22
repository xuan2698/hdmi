def reference(vectors):
    q = 0
    ena = 0
    result = []
    for row in vectors:
        rst = row.get("reset", 0)

        # upper_digit_enables: registered on posedge from pre-edge q
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        bit0 = 1 if ones == 9 else 0
        bit1 = 1 if (ones == 9 and tens == 9) else 0
        bit2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        ena_comb = bit0 + 2 * bit1 + 4 * bit2

        if rst:
            # sync_reset: synchronous active-high reset has priority over increment
            q_next = 0
            ena_next = 0
        else:
            # bcd_increment: increment 4-digit BCD counter modulo 10000
            d0 = q & 0xF
            d1 = (q >> 4) & 0xF
            d2 = (q >> 8) & 0xF
            d3 = (q >> 12) & 0xF

            d0 += 1
            if d0 == 10:
                d0 = 0
                d1 += 1
                if d1 == 10:
                    d1 = 0
                    d2 += 1
                    if d2 == 10:
                        d2 = 0
                        d3 += 1
                        if d3 == 10:
                            d3 = 0

            q_next = (d3 << 12) | (d2 << 8) | (d1 << 4) | d0

            # upper_digit_enables: registered enable from pre-edge q
            ena_next = ena_comb

        q = q_next & 0xFFFF
        ena = ena_next & 0x7
        result.append({"q": q, "ena": ena})

    return result
