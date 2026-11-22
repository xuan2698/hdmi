def reference(vectors):
    # Rule sync_active_high_reset: synchronous active-high reset clears q and ena after the rising edge.
    # Rule bcd_counter_increment: on non-reset rising edges, increment four-digit BCD count modulo 10000.
    # Rule upper_digit_enables: combinational same-cycle carry enables based on current q, ena[0]=tens, ena[1]=hundreds, ena[2]=thousands.
    q = 0
    ena = 0
    current_reset = 0
    out = []
    for v in vectors:
        if 'reset' in v:
            r = v['reset']
        else:
            r = current_reset

        if r == 1:
            q = 0
            ena = 0
        else:
            d0 = q & 15
            d1 = (q >> 4) & 15
            d2 = (q >> 8) & 15
            d3 = (q >> 12) & 15
            n = d0 + 10 * d1 + 100 * d2 + 1000 * d3
            n = (n + 1) % 10000

            d0 = n % 10
            n //= 10
            d1 = n % 10
            n //= 10
            d2 = n % 10
            n //= 10
            d3 = n % 10
            q = d0 | (d1 << 4) | (d2 << 8) | (d3 << 12)

            ones = q & 15
            tens = (q >> 4) & 15
            hundreds = (q >> 8) & 15
            ena = 0
            if ones == 9:
                ena = ena | 1
                if tens == 9:
                    ena = ena | 2
                    if hundreds == 9:
                        ena = ena | 4

        out.append({'q': q, 'ena': ena})

        if 'mid' in v:
            mid = v['mid']
            if 'reset' in mid:
                current_reset = mid['reset']
            else:
                current_reset = r
        else:
            current_reset = r

    return out
