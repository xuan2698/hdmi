def reference(vectors):
    # State: 4-digit BCD counter value
    count = 0
    outputs = []

    for vec in vectors:
        reset = vec.get("reset", 0)

        # R1_reset: synchronous active-high reset -> q=0, ena=0
        if reset == 1:
            count = 0
            q = 0
            ena = 0
        else:
            # Compute current outputs from current state (before edge)
            q = count
            ones = count & 0xF
            tens = (count >> 4) & 0xF
            hundreds = (count >> 8) & 0xF
            thousands = (count >> 12) & 0xF

            # R4_ena_tens: enable tens when ones == 9
            # R5_ena_hundreds: enable hundreds when ones==9 and tens==9
            # R6_ena_thousands: enable thousands when ones==9, tens==9, hundreds==9
            ena = 0
            if ones == 9:
                ena |= 1  # tens enable
                if tens == 9:
                    ena |= 2  # hundreds enable
                    if hundreds == 9:
                        ena |= 4  # thousands enable

            # Compute next state (posedge update)
            # R2_ones_increment / R3_ones_wrap / R7_full_wrap
            if count == 9999:
                count = 0
            else:
                ones_n = ones + 1
                if ones_n == 10:
                    ones_n = 0
                    tens_n = tens + 1
                    if tens_n == 10:
                        tens_n = 0
                        hundreds_n = hundreds + 1
                        if hundreds_n == 10:
                            hundreds_n = 0
                            thousands_n = thousands + 1
                            if thousands_n == 10:
                                thousands_n = 0
                        else:
                            thousands_n = thousands
                    else:
                        hundreds_n = hundreds
                        thousands_n = thousands
                else:
                    tens_n = tens
                    hundreds_n = hundreds
                    thousands_n = thousands
                count = (thousands_n << 12) | (hundreds_n << 8) | (tens_n << 4) | ones_n

        outputs.append({"q": q, "ena": ena})

    return outputs
