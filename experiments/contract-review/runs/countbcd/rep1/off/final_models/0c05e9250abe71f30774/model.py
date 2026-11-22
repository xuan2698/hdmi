def reference(vectors):
    # Contract implementation.
    # State: count (16-bit BCD), initialized to 0.
    # Outputs are combinational from current state (visible same cycle as state).
    # Synchronous active-high reset: on posedge with reset==1, count -> 0.
    # Otherwise on posedge, increment BCD counter.
    # ena[0] = tens enable = (ones == 9)
    # ena[1] = hundreds enable = (ones == 9 and tens == 9)
    # ena[2] = thousands enable = (ones == 9 and tens == 9 and hundreds == 9)
    # Mid changes occur after sampling, before next edge; carried to next row.

    count = 0  # R1_reset: initial state 0 (power-up unspecified but concrete)
    out = []

    for vec in vectors:
        reset = vec.get("reset", 0)

        # Compute outputs from current state (visible same cycle).
        ones = count & 0xF
        tens = (count >> 4) & 0xF
        hundreds = (count >> 8) & 0xF
        thousands = (count >> 12) & 0xF

        # R4_ena_tens, R5_ena_hundreds, R6_ena_thousands
        ena_tens = 1 if ones == 9 else 0
        ena_hundreds = 1 if (ones == 9 and tens == 9) else 0
        ena_thousands = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        ena = (ena_thousands << 2) | (ena_hundreds << 1) | ena_tens

        out.append({"q": count & 0xFFFF, "ena": ena & 0x7})

        # Process posedge: update state for next cycle.
        if reset == 1:
            # R1_reset: synchronous active-high reset
            count = 0
        else:
            # BCD increment
            if count == 0x9999:
                # R7_full_wrap: wrap to 0
                count = 0
            else:
                # R2_ones_increment / R3_ones_wrap
                ones = count & 0xF
                tens = (count >> 4) & 0xF
                hundreds = (count >> 8) & 0xF
                thousands = (count >> 12) & 0xF
                if ones != 9:
                    ones += 1
                else:
                    ones = 0
                    if tens != 9:
                        tens += 1
                    else:
                        tens = 0
                        if hundreds != 9:
                            hundreds += 1
                        else:
                            hundreds = 0
                            if thousands != 9:
                                thousands += 1
                            else:
                                thousands = 0
                count = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones

    return out
