def reference(vectors):
    # Contract:
    # - full_module is a 3-bit loadable feedback register.
    # - On posedge clk: if L==1, q <= r; else q <= {q[1]^q[2], q[0], q[2]}.
    # - Sample after posedge settles; mid changes affect next edge.
    # - Return dict with 'Q' as unsigned int in [0,7] for each row.
    q = 0  # power-up unspecified; use 0 as concrete value
    out = []
    for row in vectors:
        # Apply inputs driven before the sampled edge
        L = row.get('L', 0) & 1
        r = row.get('r', 0) & 7
        # Compute next state at posedge
        if L:
            q_next = r
        else:
            q_next = (((q >> 1) & 1) ^ ((q >> 2) & 1)) << 2
            q_next |= (q & 1) << 1
            q_next |= (q >> 2) & 1
        q = q_next & 7
        # Mid-cycle changes occur after sampling; they don't affect this row's Q
        out.append({'Q': q})
    return out
