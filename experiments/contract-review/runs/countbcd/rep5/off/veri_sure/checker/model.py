def reference(vectors):
    # Contract:
    # - clk posedge: synchronous active-high reset clears q and ena.
    # - Otherwise BCD increment with carry; ena[i] indicates upper digit increments.
    # - Outputs are registered (latency 1 cycle): q/ena reflect state after sampled edge.
    # - Mid input changes occur AFTER sampling, before next edge.
    # State is initialized to 0 (power-up unspecified but must be concrete).
    q = 0
    ena = 0
    out = []
    for row in vectors:
        # Apply mid changes from previous row are already in row inputs.
        reset = row.get('reset', 0)
        # Sample on posedge: compute next state from current inputs and state.
        if reset:
            nq = 0
            nena = 0
        else:
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF
            # ena computed from pre-increment digits
            e0 = 1 if ones == 9 else 0
            e1 = 1 if (ones == 9 and tens == 9) else 0
            e2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
            nena = (e2 << 2) | (e1 << 1) | e0
            # increment
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
            nq = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones
        q = nq
        ena = nena
        out.append({'q': q, 'ena': ena})
    return out
