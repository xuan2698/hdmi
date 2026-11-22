def reference(vectors):
    # q_sync_reset: synchronous active-high reset sets q to 0 at posedge.
    # q_bcd_count: BCD increment on posedge when reset == 0.
    # ena_upper_digit_increment: candidate interpretation: ena reflects the
    # increment performed on this edge, computed from the pre-edge q.
    q = 0
    reset_state = 0
    out = []
    for row in vectors:
        # Drive row inputs before the sampled posedge.
        if "reset" in row:
            reset_state = row["reset"]

        if reset_state:
            # q_sync_reset: reset has priority; no BCD increment.
            ena = 0
            new_q = 0
        else:
            # Extract pre-edge BCD digits.
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF

            # ena_upper_digit_increment: carry enables for digits [3:1]
            # on the edge just sampled (pre-edge digit values).
            bit0 = 1 if ones == 9 else 0
            bit1 = 1 if (ones == 9 and tens == 9) else 0
            bit2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
            ena = bit0 | (bit1 << 1) | (bit2 << 2)

            # q_bcd_count: BCD increment with carry.
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

            new_q = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones

        q = new_q & 0xFFFF
        out.append({"q": q, "ena": ena & 0x7})

        # Optional mid input changes occur after sampling and are carried
        # to the start of the next row.
        if "mid" in row:
            mid = row["mid"]
            try:
                if "reset" in mid:
                    reset_state = mid["reset"]
            except:
                # If mid encodes the reset value directly, use it.
                reset_state = mid

    return out
