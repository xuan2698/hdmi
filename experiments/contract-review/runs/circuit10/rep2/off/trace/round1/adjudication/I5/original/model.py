def reference(vectors):
    # Contract implementation.
    # R1: state is a single flip-flop updated on posedge clk to a XOR b.
    # R2: q is combinational, equal to a XOR b of current inputs.
    # Reset: none. Power-up state is unspecified; we model it as 0 initially
    # and only update on posedge clk (sampled after edge settles).
    # Mid-cycle input changes occur after sampling and carry to next row.

    state = 0  # power-up unspecified; concrete default
    out = []

    for vec in vectors:
        clk = vec.get('clk', 0)
        a = vec.get('a', 0)
        b = vec.get('b', 0)

        # R2: combinational q = a XOR b (same cycle)
        q = (a ^ b) & 1

        # R1: on posedge clk, state updates to a XOR b (visible next cycle)
        if clk == 1:
            state = (a ^ b) & 1

        out.append({'q': q & 1, 'state': state & 1})

    return out
