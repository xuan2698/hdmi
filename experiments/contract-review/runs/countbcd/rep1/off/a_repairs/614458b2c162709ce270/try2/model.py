def reference(vectors):
    # Contract implementation.
    # State: count (16-bit BCD), initialized to 0.
    # Outputs q (16-bit) and ena (3-bit) are combinational from state.
    # Synchronous active-high reset: on posedge clk with reset==1, count <= 0.
    # Otherwise count increments as BCD counter.
    # ena[0] = (ones == 9)  -> tens increments
    # ena[1] = (ones == 9 and tens == 9) -> hundreds increments
    # ena[2] = (ones == 9 and tens == 9 and hundreds == 9) -> thousands increments
    # R7: full wrap 9999 -> 0000 (selected interpretation).

    count = 0  # R1_reset: initial state 0 (power-up unspecified but concrete)
    results = []

    for vec in vectors:
        reset = vec.get('reset', 0)

        # Compute outputs from current state (visible same cycle for reset,
        # next cycle for increments -- but outputs are just combinational
        # from state, so we output current state's q and ena).
        q = count
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        thousands = (q >> 12) & 0xF

        ena = 0
        if ones == 9:
            ena |= 1  # R4_ena_tens
        if ones == 9 and tens == 9:
            ena |= 2  # R5_ena_hundreds
        if ones == 9 and tens == 9 and hundreds == 9:
            ena |= 4  # R6_ena_thousands

        results.append({'q': q, 'ena': ena})

        # Clock edge: update state
        if reset == 1:
            # R1_reset: synchronous active-high reset
            count = 0
        else:
            # BCD increment
            if q == 0x9999:
                # R7_full_wrap: wrap to 0000
                count = 0
            else:
                # R2_ones_increment / R3_ones_wrap
                new_ones = ones + 1
                carry = 0
                if new_ones == 10:
                    new_ones = 0
                    carry = 1
                new_tens = tens + carry
                carry2 = 0
                if new_tens == 10:
                    new_tens = 0
                    carry2 = 1
                new_hundreds = hundreds + carry2
                carry3 = 0
                if new_hundreds == 10:
                    new_hundreds = 0
                    carry3 = 1
                new_thousands = thousands + carry3
                if new_thousands == 10:
                    new_thousands = 0
                count = (new_thousands << 12) | (new_hundreds << 8) | (new_tens << 4) | new_ones

    return results
