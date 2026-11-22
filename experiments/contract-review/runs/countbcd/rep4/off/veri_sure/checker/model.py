def reference(vectors):
    # Contract:
    # - Synchronous active-high reset: on posedge with reset=1, q<=0 and ena<=0.
    # - Otherwise ones digit increments mod 10; cascading when lower digits are 9.
    # - ena[0]=1 iff q[3:0]==9; ena[1]=1 iff q[3:0]==9 and q[7:4]==9;
    #   ena[2]=1 iff q[3:0]==9, q[7:4]==9, q[11:8]==9.
    # - Outputs have latency 1: they reflect state after the sampled posedge.
    # - Mid input changes occur AFTER sampling, before the next edge.
    q = 0
    ena = 0
    out = []
    for row in vectors:
        # Apply mid changes from previous row (already applied before this row's sampling)
        # Sample at posedge: compute next state from current inputs/state
        reset = row.get('reset', 0)
        if reset:
            nq = 0
            nena = 0
        else:
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF
            ena0 = 1 if ones == 9 else 0
            ena1 = 1 if (ones == 9 and tens == 9) else 0
            ena2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
            nena = ena0 | (ena1 << 1) | (ena2 << 2)
            # increment
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
            nq = ones | (tens << 4) | (hundreds << 8) | (thousands << 12)
        q = nq
        ena = nena
        out.append({'q': q, 'ena': ena})
    return out
