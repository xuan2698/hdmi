def reference(vectors):
    # Concrete named state: n is the current decimal counter value 0..9999.
    # Power-up is unspecified by the spec; use concrete initial value 0.
    n = 0
    result = []

    for row in vectors:
        # sync_reset: read reset driven before the sampled posedge.
        reset = row.get("reset", 0)

        # posedge clk after settled: synchronous active-high reset has priority.
        if reset == 1:
            # sync_reset: reset clears the counter to 0 and overrides counting.
            n = 0
        else:
            # bcd_increment: unresolved candidate interpretation applied:
            # down-count by 1 modulo 10000 on each enabled posedge.
            if n == 0:
                n = 9999
            else:
                n = n - 1

        # Decode the BCD digits from the settled post-edge state.
        ones = n % 10
        tens = (n // 10) % 10
        hundreds = (n // 100) % 10
        thousands = (n // 1000) % 10

        # q: 16-bit packed BCD, q[3:0]=ones, ..., q[15:12]=thousands.
        q = ones + (tens << 4) + (hundreds << 8) + (thousands << 12)

        # upper_digit_enables: combinational from current q/post-edge n.
        # bit0=tens enable, bit1=hundreds enable, bit2=thousands enable.
        b0 = 1 if ones == 9 else 0
        b1 = 1 if (ones == 9 and tens == 9) else 0
        b2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        ena = b0 + 2 * b1 + 4 * b2

        result.append({"q": q, "ena": ena})

    return result
