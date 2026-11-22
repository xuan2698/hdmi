def reference(vectors):
    # Contract implementation.
    # R1: state <= q on negedge (visible next cycle). We model state as the
    #     flip-flop value that will be captured; q is combinational from state.
    # R2: q = state XOR a XOR b (combinational, same cycle).
    # Power-up unspecified: start state at 0 (concrete).
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0) & 1
        b = v.get('b', 0) & 1
        # R2: combinational output using current state
        q = (state ^ a ^ b) & 1
        out.append({'q': q, 'state': state})
        # R1: negedge captures q into state for next cycle
        state = q
    return out
