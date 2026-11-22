def reference(vectors):
    # State: 16-bit BCD counter value
    q = 0
    # Registered enable outputs (3 bits: [2]=thousands, [1]=hundreds, [0]=tens)
    ena = 0
    out = []
    for row in vectors:
        reset = row.get('reset', 0)
        # R1_reset: synchronous active-high reset, visible same cycle
        # (reset is sampled at posedge; outputs reflect post-edge state)
        if reset == 1:
            q = 0
            ena = 0
        else:
            # Compute enables based on current q BEFORE increment (registered)
            # R3_ena_tens: q[3:0]==9
            # R4_ena_hundreds: q[3:0]==9 and q[7:4]==9
            # R5_ena_thousands: q[3:0]==9 and q[7:4]==9 and q[11:8]==9
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF
            e_tens = 1 if ones == 9 else 0
            e_hundreds = 1 if (ones == 9 and tens == 9) else 0
            e_thousands = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
            # Candidate interpretation: ena registered one cycle after q[3:0]==9
            # So ena output reflects enables computed from PREVIOUS q state.
            # We store new ena for next cycle, output current ena.
            new_ena = (e_thousands << 2) | (e_hundreds << 1) | e_tens
            # R2_ones_increment / R6_bcd_rollover: increment BCD counter
            ones_n = ones + 1
            if ones_n == 10:
                ones_n = 0
                tens_n = tens + 1
                if tens_n == 10:
                    tens_n = 0
                    hundreds_n = hundreds + 1
                    if hundreds_n == 10:
                        hundreds_n = 0
                        thousands_n = (thousands + 1) % 10
                    else:
                        thousands_n = thousands
                else:
                    hundreds_n = hundreds
                    thousands_n = thousands
            else:
                tens_n = tens
                hundreds_n = hundreds
                thousands_n = thousands
            q = (thousands_n << 12) | (hundreds_n << 8) | (tens_n << 4) | ones_n
            ena = new_ena
        out.append({'q': q & 0xFFFF, 'ena': ena & 0x7})
    return out
