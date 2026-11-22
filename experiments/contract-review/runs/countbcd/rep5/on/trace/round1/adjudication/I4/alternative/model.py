def reference(vectors):
    # State q is the packed 16-bit BCD counter value.
    q = 0
    outputs = []

    for vec in vectors:
        # Inputs for this row are driven before the sampled posedge.
        reset = int(vec.get('reset', 0)) & 1

        # Rule sync_reset: synchronous active-high reset has priority.
        # Candidate interpretation: reset sets q to BCD 9999 (0x9999) instead of 0.
        if reset:
            q = 0x9999
        else:
            # Rule bcd_increment: increment packed BCD modulo 10000.
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF

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

            q = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones

        # Rule upper_digit_enables: combinational from current q after the edge.
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF

        bit0 = 1 if ones == 9 else 0
        bit1 = 1 if (ones == 9 and tens == 9) else 0
        bit2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        ena = bit0 + 2 * bit1 + 4 * bit2

        outputs.append({
            'q': q & 0xFFFF,
            'ena': ena & 0x7
        })

    return outputs
