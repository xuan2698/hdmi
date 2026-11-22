def reference(vectors):
    # Contract implementation.
    # State: count (16-bit BCD, q[3:0]=ones, q[7:4]=tens, q[11:8]=hundreds, q[15:12]=thousands)
    # Synchronous active-high reset. Outputs visible same cycle (combinational from state).
    # R1_reset: reset==1 -> q=0, ena=0 (sync, same_cycle)
    # R2_ones_increment: ones increments by 1 when not 9 (next_cycle)
    # R3_ones_wrap: ones 9 -> 0, tens increments (next_cycle)
    # R4_ena_tens: ena[0]=1 when ones==9 (same_cycle)
    # R5_ena_hundreds: ena[1]=1 when ones==9 and tens==9 (same_cycle)
    # R6_ena_thousands: ena[2]=1 when ones==9 and tens==9 and hundreds==9 (same_cycle)
    # R7_full_wrap: 9999 -> 0000 (next_cycle)

    count = 0
    results = []

    for vec in vectors:
        reset = vec.get('reset', 0)

        # Compute outputs from current state (same_cycle visibility)
        ones = count & 0xF
        tens = (count >> 4) & 0xF
        hundreds = (count >> 8) & 0xF
        thousands = (count >> 12) & 0xF

        # R4_ena_tens, R5_ena_hundreds, R6_ena_thousands
        ena = 0
        if ones == 9:
            ena |= 1  # R4_ena_tens
            if tens == 9:
                ena |= 2  # R5_ena_hundreds
                if hundreds == 9:
                    ena |= 4  # R6_ena_thousands

        if reset:
            # R1_reset: outputs forced to 0 same cycle
            results.append({'q': 0, 'ena': 0})
            # state update on posedge: reset -> 0
            count = 0
        else:
            results.append({'q': count, 'ena': ena})
            # Next-state computation (posedge)
            # R2_ones_increment / R3_ones_wrap / R7_full_wrap
            if count == 9999:
                count = 0  # R7_full_wrap
            else:
                if ones != 9:
                    count = count + 1  # R2_ones_increment
                else:
                    # R3_ones_wrap: ones -> 0, tens increments
                    new_ones = 0
                    new_tens = tens + 1
                    new_hundreds = hundreds
                    new_thousands = thousands
                    if new_tens == 10:
                        new_tens = 0
                        new_hundreds += 1
                        if new_hundreds == 10:
                            new_hundreds = 0
                            new_thousands += 1
                            if new_thousands == 10:
                                new_thousands = 0
                    count = (new_thousands << 12) | (new_hundreds << 8) | (new_tens << 4) | new_ones

    return results
