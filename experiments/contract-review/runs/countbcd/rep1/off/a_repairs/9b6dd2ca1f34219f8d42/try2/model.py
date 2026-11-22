def reference(vectors):
    # Contract implementation for 4-digit BCD counter.
    # State: count (16-bit BCD), initialized to 0.
    # Outputs: q (16-bit), ena (3-bit).
    # Rules:
    # R1_reset: sync active-high reset -> q=0, ena=0 (same cycle visible)
    # R2_ones_increment: if reset==0 and q[3:0]!=9 -> q increments ones (next cycle)
    # R3_ones_wrap: if reset==0 and q[3:0]==9 and q[7:4]!=9 -> ones wraps, tens increments
    # R4_ena_tens: ena[0]=1 when reset==0 and q[3:0]==9 (same cycle)
    # R5_ena_hundreds: ena[1]=1 when reset==0 and q[3:0]==9 and q[7:4]==9 (same cycle)
    # R6_ena_thousands: ena[2]=1 when reset==0 and q[3:0]==9 and q[7:4]==9 and q[11:8]==9 (same cycle)
    # R7_full_wrap: if reset==0 and q==0x9999 -> q wraps to 0 (next cycle)
    # R8_ena_default: ena default 0 when not all conditions

    count = 0  # R1_reset: initial state after reset
    results = []

    for vec in vectors:
        reset = vec.get('reset', 0)

        # Compute outputs based on current state (before posedge update)
        # R1_reset: reset visible same cycle
        if reset == 1:
            q_out = 0
            ena_out = 0
        else:
            q_out = count
            # R4_ena_tens, R5_ena_hundreds, R6_ena_thousands
            ones = count & 0xF
            tens = (count >> 4) & 0xF
            hundreds = (count >> 8) & 0xF
            thousands = (count >> 12) & 0xF
            ena_out = 0
            if ones == 9:
                ena_out |= 1  # R4_ena_tens
                if tens == 9:
                    ena_out |= 2  # R5_ena_hundreds
                    if hundreds == 9:
                        ena_out |= 4  # R6_ena_thousands

        results.append({'q': q_out & 0xFFFF, 'ena': ena_out & 0x7})

        # Update state at posedge (next cycle)
        if reset == 1:
            count = 0  # R1_reset
        else:
            ones = count & 0xF
            tens = (count >> 4) & 0xF
            hundreds = (count >> 8) & 0xF
            thousands = (count >> 12) & 0xF

            if count == 0x9999:
                count = 0  # R7_full_wrap
            else:
                # Increment BCD
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
                count = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones

    return results
