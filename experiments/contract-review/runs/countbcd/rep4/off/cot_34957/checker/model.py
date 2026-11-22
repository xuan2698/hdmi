def reference(vectors):
    # Contract:
    # - q is a 16-bit BCD counter: q[3:0]=ones, q[7:4]=tens, q[11:8]=hundreds, q[15:12]=thousands.
    # - ena[0] = tens enable  = (ones == 9)
    # - ena[1] = hundreds enable = (tens == 9 and ones == 9)
    # - ena[2] = thousands enable = (hundreds == 9 and tens == 9 and ones == 9)
    # - ena is combinational from current q (and forced low when reset is high).
    # - Synchronous active-high reset: on posedge with reset=1, q <= 0.
    # - Otherwise increment BCD with carry.
    # - Rows before first observed reset=1 are don't-care; we still emit concrete values.
    # - Mid input changes occur after sampling and apply to the next row.

    out = []
    q = 0
    known = False  # becomes True after first sampled reset=1

    for row in vectors:
        # Snapshot inputs at the sampled posedge
        reset = row.get('reset', 0) & 1
        # q is our internal state (the sampled q for this row)
        cur_q = q

        # Compute combinational enables from current state snapshot
        ones = cur_q & 0xF
        tens = (cur_q >> 4) & 0xF
        hundreds = (cur_q >> 8) & 0xF
        thousands = (cur_q >> 12) & 0xF

        if reset:
            ena = 0
        else:
            e0 = 1 if ones == 9 else 0
            e1 = 1 if (tens == 9 and ones == 9) else 0
            e2 = 1 if (hundreds == 9 and tens == 9 and ones == 9) else 0
            ena = e0 | (e1 << 1) | (e2 << 2)

        # Compute next state
        if reset:
            next_q = 0
            known = True
        else:
            # BCD increment
            n_ones = ones + 1
            carry1 = 0
            if n_ones == 10:
                n_ones = 0
                carry1 = 1
            n_tens = tens + carry1
            carry2 = 0
            if n_tens == 10:
                n_tens = 0
                carry2 = 1
            n_hundreds = hundreds + carry2
            carry3 = 0
            if n_hundreds == 10:
                n_hundreds = 0
                carry3 = 1
            n_thousands = thousands + carry3
            if n_thousands == 10:
                n_thousands = 0
            next_q = (n_thousands << 12) | (n_hundreds << 8) | (n_tens << 4) | n_ones

        # Emit outputs for this row
        out.append({'q': cur_q & 0xFFFF, 'ena': ena & 0x7})

        # Advance state
        q = next_q

    return out
