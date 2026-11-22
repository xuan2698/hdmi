def reference(vectors):
    # Contract implementation for 4-digit BCD counter.
    # State: count (16-bit BCD), initialized to 0.
    # Outputs: q (16-bit), ena (3-bit).
    # Rules:
    # R1_reset: sync active-high reset -> q=0, ena=0 same cycle.
    # R2_ones_increment: if reset==0 and ones!=9, ones increments next cycle.
    # R3_ones_wrap: if ones==9 and tens!=9, ones=0, tens++ next cycle.
    # R4_ena_tens: ena[0]=1 when ones==9 (same cycle).
    # R5_ena_hundreds: ena[1]=1 when ones==9 and tens==9 (same cycle).
    # R6_ena_thousands: ena[2]=1 when ones==9 and tens==9 and hundreds==9 (same cycle).
    # R7_full_wrap: if q==0x9999, wrap to 0 next cycle.
    # R8_ena_default: ena computed from current q each cycle.

    # Initialize state
    count = 0  # 16-bit BCD value

    results = []
    for vec in vectors:
        reset = vec.get('reset', 0)

        # Compute outputs based on current state (before posedge update)
        # R1_reset: during reset, outputs are 0
        if reset == 1:
            q_out = 0
            ena_out = 0
        else:
            q_out = count
            # Compute ena from current q
            ones = count & 0xF
            tens = (count >> 4) & 0xF
            hundreds = (count >> 8) & 0xF
            thousands = (count >> 12) & 0xF
            ena_bits = 0
            if ones == 9:
                ena_bits |= 1  # R4_ena_tens
                if tens == 9:
                    ena_bits |= 2  # R5_ena_hundreds
                    if hundreds == 9:
                        ena_bits |= 4  # R6_ena_thousands
            ena_out = ena_bits

        results.append({'q': q_out, 'ena': ena_out})

        # Update state at posedge (after sampling)
        if reset == 1:
            # R1_reset: synchronous reset
            count = 0
        else:
            # Increment BCD counter
            ones = count & 0xF
            tens = (count >> 4) & 0xF
            hundreds = (count >> 8) & 0xF
            thousands = (count >> 12) & 0xF

            if count == 0x9999:
                # R7_full_wrap
                count = 0
            else:
                # R2_ones_increment / R3_ones_wrap
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

    return results
