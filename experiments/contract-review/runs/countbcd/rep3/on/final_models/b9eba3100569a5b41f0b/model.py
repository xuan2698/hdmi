def reference(vectors):
    # Rule q_sync_reset: synchronous active-high reset sets q to 0 at posedge clk.
    # Rule q_bcd_count: when reset is low, increment the 4-digit BCD counter.
    # Rule ena_upper_digit_increment: ena is combinational from settled q.

    q = 0
    reset_value = 0
    results = []

    for row in vectors:
        # Inputs are driven before the sampled posedge. Retain prior value if omitted.
        if "reset" in row:
            reset_value = row["reset"] & 1

        if reset_value:
            q = 0
        else:
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

            q = d0 | (d1 << 4) | (d2 << 8) | (d3 << 12)

        # Combinational enable from settled q after the posedge update.
        d0 = q & 0xF
        d1 = (q >> 4) & 0xF
        d2 = (q >> 8) & 0xF

        ena = 0
        if d0 == 9:
            ena |= 1
            if d1 == 9:
                ena |= 2
                if d2 == 9:
                    ena |= 4

        results.append({
            "ena": ena & 0x7,
            "q": q & 0xFFFF
        })

    return results
