def reference(vectors):
    # State: current BCD counter value (16-bit) and reset flag
    # Contract rules:
    # R1_reset: synchronous active-high reset -> q=0, ena=0 on posedge when reset==1
    # R2_ones_count: ones digit increments when != 9
    # R3_ones_wrap: ones digit wraps 9->0, carry to tens
    # R4_tens_increment: tens increments when ones==9 and tens!=9
    # R5_tens_wrap: tens wraps 9->0, carry to hundreds
    # R6_hundreds_increment: hundreds increments when ones==9 and tens==9 and hundreds!=9
    # R7_thousands_increment: thousands increments when ones==9,tens==9,hundreds==9 and thousands!=9
    # R8_full_wrap: full wrap 9999->0
    # R9_ena_tens: ena[2] (tens enable) = (ones==9)
    # R10_ena_hundreds: ena[1] (hundreds enable) = (ones==9 and tens==9)
    # R11_ena_thousands: ena[0] (thousands enable) = (ones==9 and tens==9 and hundreds==9)
    # global: ena[0]=digit3(thousands), ena[1]=digit2(hundreds), ena[2]=digit1(tens)

    q = 0  # current counter value
    results = []

    for vec in vectors:
        reset = vec.get('reset', 0)

        # Compute ena combinationally from current q (before posedge update)
        # R9_ena_tens / R10_ena_hundreds / R11_ena_thousands
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        thousands = (q >> 12) & 0xF

        ena_tens = 1 if ones == 9 else 0
        ena_hundreds = 1 if (ones == 9 and tens == 9) else 0
        ena_thousands = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0

        # global: ena[0]=thousands, ena[1]=hundreds, ena[2]=tens
        ena = (ena_thousands << 0) | (ena_hundreds << 1) | (ena_tens << 2)

        # Output for this row is the state BEFORE the posedge update
        # (values driven before sampled edge)
        results.append({'q': q, 'ena': ena})

        # Now apply posedge update for next cycle
        if reset == 1:
            # R1_reset
            q = 0
        else:
            # Compute next BCD value
            if ones != 9:
                # R2_ones_count
                q = q + 1
            else:
                # ones == 9, wrap
                if tens != 9:
                    # R3_ones_wrap + R4_tens_increment
                    q = (q & ~0xFF) | ((tens + 1) << 4) | 0
                else:
                    # tens == 9
                    if hundreds != 9:
                        # R5_tens_wrap + R6_hundreds_increment
                        q = (q & ~0xFFF) | ((hundreds + 1) << 8) | 0
                    else:
                        # hundreds == 9
                        if thousands != 9:
                            # R7_thousands_increment
                            q = ((thousands + 1) << 12) | 0
                        else:
                            # R8_full_wrap
                            q = 0

    return results
