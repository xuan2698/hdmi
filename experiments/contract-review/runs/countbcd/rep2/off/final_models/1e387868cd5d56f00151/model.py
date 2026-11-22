def reference(vectors):
    # State: 4-digit BCD counter value (16 bits)
    # q[3:0]=ones, q[7:4]=tens, q[11:8]=hundreds, q[15:12]=thousands
    count = 0
    out = []

    for vec in vectors:
        reset = vec.get("reset", 0)

        # R1_reset: synchronous active-high reset -> outputs 0 same cycle
        if reset == 1:
            q = 0
            ena = 0
            # state update on posedge (reset)
            count = 0
        else:
            # Compute current outputs from current state (before edge)
            ones = count & 0xF
            tens = (count >> 4) & 0xF
            hundreds = (count >> 8) & 0xF
            thousands = (count >> 12) & 0xF

            # R4_ena_tens: ena[0] when ones==9
            ena_tens = 1 if ones == 9 else 0
            # R5_ena_hundreds: ena[1] when ones==9 and tens==9
            ena_hundreds = 1 if (ones == 9 and tens == 9) else 0
            # R6_ena_thousands: ena[2] when ones==9 and tens==9 and hundreds==9
            ena_thousands = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0

            ena = (ena_thousands << 2) | (ena_hundreds << 1) | ena_tens
            q = count

            # Compute next state (posedge update)
            # R2_ones_increment / R3_ones_wrap / R7_full_wrap
            if count == 9999:
                # R7_full_wrap: wrap to 0
                count = 0
            else:
                # Increment BCD
                new_ones = ones + 1
                new_tens = tens
                new_hundreds = hundreds
                new_thousands = thousands
                if new_ones == 10:
                    new_ones = 0
                    new_tens += 1
                    if new_tens == 10:
                        new_tens = 0
                        new_hundreds += 1
                        if new_hundreds == 10:
                            new_hundreds = 0
                            new_thousands += 1
                            if new_thousands == 10:
                                new_thousands = 0
                count = (new_thousands << 12) | (new_hundreds << 8) | (new_tens << 4) | new_ones

        out.append({"q": q & 0xFFFF, "ena": ena & 0x7})

    return out
