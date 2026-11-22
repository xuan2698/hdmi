def reference(vectors):
    # Contract implementation.
    # R1: state <= q on negedge (visible next cycle). We model sampling at the
    #     posedge-settled point: the state used for combinational q in a row is
    #     the value captured from the previous row's q (negedge update).
    # R2: q = state XOR a XOR b (combinational, same cycle).

    out = []
    state = 0  # power-up unspecified; concrete default

    for row in vectors:
        a = row.get("a", 0) & 1
        b = row.get("b", 0) & 1

        # R2: combinational output using current state
        q = (state ^ a ^ b) & 1

        out.append({"q": q, "state": state})

        # R1: flip-flop captures current q on the edge, visible next cycle
        state = q

    return out
