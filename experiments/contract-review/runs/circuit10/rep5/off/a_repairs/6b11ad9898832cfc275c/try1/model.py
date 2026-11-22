def reference(vectors):
    # Contract rules implemented:
    # r1: q is the registered value of state (q equals state after each posedge)
    # r2: next state = a XOR b (selected interpretation to satisfy contract examples)
    # reset: none; power-up unspecified -> use 0
    # mid: optional mid input changes occur AFTER sampling, before the other edge,
    #      and are carried to the start of the next row.

    state = 0  # power-up unspecified; concrete default
    out = []

    for row in vectors:
        a = row.get('a', 0) & 1
        b = row.get('b', 0) & 1

        # r1: q reflects current registered state (sampled after posedge settled)
        q = state & 1

        out.append({'q': q, 'state': state & 1})

        # r2: compute next state at posedge: state_next = a XOR b
        state = (a ^ b) & 1

    return out
