def reference(vectors):
    # State: 16-bit BCD counter value
    q = 0
    # Outputs are combinational from state (visible same cycle as posedge update)
    # We model: at each posedge, if reset -> q=0; else q increments per BCD rules.
    # ena is computed from the CURRENT q (before increment) per rules R3-R5,
    # but "visible same_cycle" means ena reflects the value that triggers increment.
    # Candidate interpretation: ena[0]=thousands, ena[1]=hundreds, ena[2]=tens (reversed mapping)
    results = []
    for row in vectors:
        reset = row.get('reset', 0)
        # Compute outputs based on current state BEFORE the posedge update,
        # since ena indicates when upper digits should be incremented at this edge.
        # R1_reset: reset==1 -> q=0, ena=0 (synchronous, visible same cycle)
        if reset == 1:
            # R1_reset: synchronous active-high reset
            out_q = 0
            out_ena = 0
            q = 0
        else:
            # ena computed from current q (the value before increment)
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF
            # R3_ena_tens: tens increments when ones==9
            ena_tens = 1 if ones == 9 else 0
            # R4_ena_hundreds: hundreds increments when ones==9 and tens==9
            ena_hundreds = 1 if (ones == 9 and tens == 9) else 0
            # R5_ena_thousands: thousands increments when ones==9, tens==9, hundreds==9
            ena_thousands = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
            # Candidate interpretation: ena[0]=thousands, ena[1]=hundreds, ena[2]=tens
            out_ena = (ena_thousands << 0) | (ena_hundreds << 1) | (ena_tens << 2)
            out_q = q
            # Now perform the increment for next state (R2, R6)
            # R2_ones_increment: ones digit increments each cycle
            new_ones = (ones + 1) % 10
            carry = 1 if ones == 9 else 0
            new_tens = tens
            if carry:
                new_tens = (tens + 1) % 10
                carry = 1 if tens == 9 else 0
            else:
                carry = 0
            new_hundreds = hundreds
            if carry:
                new_hundreds = (hundreds + 1) % 10
                carry = 1 if hundreds == 9 else 0
            else:
                carry = 0
            new_thousands = thousands
            if carry:
                new_thousands = (thousands + 1) % 10
            q = (new_thousands << 12) | (new_hundreds << 8) | (new_tens << 4) | new_ones
        results.append({"q": out_q, "ena": out_ena})
    return results
