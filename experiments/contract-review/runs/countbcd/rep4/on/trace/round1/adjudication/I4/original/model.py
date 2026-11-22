def reference(vectors):
    # Power-up is unspecified; choose a concrete initial state.
    q = 0
    ena = 0
    result = []

    for row in vectors:
        reset = row["reset"]

        # sync_active_high_reset: synchronous active-high reset has priority;
        # at posedge with reset=1, q and ena become 0.
        if reset:
            q = 0
            ena = 0
        else:
            # bcd_counter_increment: increment packed BCD modulo 10000.
            d0 = q & 15
            d1 = (q >> 4) & 15
            d2 = (q >> 8) & 15
            d3 = (q >> 12) & 15

            d0 = d0 + 1
            if d0 == 10:
                d0 = 0
                d1 = d1 + 1
                if d1 == 10:
                    d1 = 0
                    d2 = d2 + 1
                    if d2 == 10:
                        d2 = 0
                        d3 = d3 + 1
                        if d3 == 10:
                            d3 = 0

            q = d0 | (d1 << 4) | (d2 << 8) | (d3 << 12)

            # upper_digit_enables: combinational enables for the upper three digits,
            # based on the current BCD count q.
            e0 = q & 15
            e1 = (q >> 4) & 15
            e2 = (q >> 8) & 15

            ena = 0
            if e0 == 9:
                ena = ena | 1
                if e1 == 9:
                    ena = ena | 2
                    if e2 == 9:
                        ena = ena | 4

        result.append({"q": q, "ena": ena})

    return result
