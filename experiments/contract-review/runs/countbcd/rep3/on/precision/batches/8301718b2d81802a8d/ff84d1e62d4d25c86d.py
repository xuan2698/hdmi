def reference(vectors):
    # State: q is the 16-bit four-digit BCD counter.
    # Power-up is unspecified, but a concrete value is required; use 0.
    q = 0
    current_reset = 0
    results = []

    for row in vectors:
        # Apply input values driven before the sampled posedge.
        if 'reset' in row:
            current_reset = row['reset'] & 1
        if 'inputs' in row:
            inp = row['inputs']
            if inp:
                if 'reset' in inp:
                    current_reset = inp['reset'] & 1

        # Rule q_sync_reset: synchronous active-high reset has priority.
        # Rule q_bcd_count: otherwise increment as a 4-digit BCD counter.
        if current_reset:
            q = 0
        else:
            d0 = q & 15
            d1 = (q >> 4) & 15
            d2 = (q >> 8) & 15
            d3 = (q >> 12) & 15

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

            q = (d3 << 12) | (d2 << 8) | (d1 << 4) | d0

        # Rule ena_upper_digit_increment: combinational from settled q.
        d0 = q & 15
        d1 = (q >> 4) & 15
        d2 = (q >> 8) & 15

        ena = 0
        if d0 == 9:
            ena = 1
            if d1 == 9:
                ena = ena | 2
                if d2 == 9:
                    ena = ena | 4

        results.append({'q': q, 'ena': ena})

        # Process optional mid changes after sampling, carried to next row.
        if 'mid' in row:
            mid = row['mid']
            if mid:
                if 'reset' in mid:
                    current_reset = mid['reset'] & 1
                if 'inputs' in mid:
                    mi = mid['inputs']
                    if mi:
                        if 'reset' in mi:
                            current_reset = mi['reset'] & 1

    return results
