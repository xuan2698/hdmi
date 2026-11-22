def reference(vectors):
    # Contract implementation.
    # State: count (16-bit BCD), initialized to 0.
    # Outputs: q (16-bit), ena (3-bit).
    # ena[0]=tens enable, ena[1]=hundreds enable, ena[2]=thousands enable.
    # Synchronous active-high reset: on posedge with reset==1, q<=0, ena<=0.
    # Otherwise on posedge: increment BCD counter, compute ena from current q.

    q = 0  # R1_reset: initial state value (power-up unspecified, use 0)
    results = []

    for row in vectors:
        reset = row.get('reset', 0)

        # Compute outputs visible "same_cycle" based on current state q
        # R4_ena_tens: ena[0] = 1 when q[3:0]==9
        # R5_ena_hundreds: ena[1] = 1 when q[3:0]==9 and q[7:4]==9
        # R6_ena_thousands: ena[2] = 1 when q[3:0]==9 and q[7:4]==9 and q[11:8]==9
        # R8_ena_default: otherwise 0
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        thousands = (q >> 12) & 0xF

        if reset:
            # R1_reset: synchronous reset forces outputs to 0 same cycle
            ena = 0
            out_q = 0
        else:
            ena = 0
            if ones == 9:
                ena |= 1  # R4_ena_tens
                if tens == 9:
                    ena |= 2  # R5_ena_hundreds
                    if hundreds == 9:
                        ena |= 4  # R6_ena_thousands
            out_q = q

        results.append({'q': out_q, 'ena': ena})

        # State update at posedge (next cycle)
        if reset:
            # R1_reset: q <= 0
            q = 0
        else:
            # BCD increment
            if q == 0x9999:
                # R7_full_wrap: wrap to 0
                q = 0
            else:
                # R2_ones_increment / R3_ones_wrap
                ones = q & 0xF
                tens = (q >> 4) & 0xF
                hundreds = (q >> 8) & 0xF
                thousands = (q >> 12) & 0xF
                if ones != 9:
                    # R2_ones_increment
                    ones += 1
                else:
                    # R3_ones_wrap
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
                q = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones

    return results
