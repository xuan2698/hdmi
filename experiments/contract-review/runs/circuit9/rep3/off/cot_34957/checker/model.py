def reference(vectors):
    # Sequential 3-bit state machine.
    # Contract:
    #  - q is the settled state after each sampled posedge.
    #  - The input actually sampled at a posedge is the carried value of `a`
    #    from the previous row's post-sample change (or the initial row's a).
    #  - Transition: if sampled a == 1 -> hold q; if sampled a == 0 -> (q+1) mod 7.
    #  - Power-up q is unspecified; first settled value is taken from the trace.
    #  - Mid-cycle changes to `a` occur after sampling and carry to next row.
    results = []
    state = None
    carried_a = None
    for row in vectors:
        clk = row.get('clk')
        a = row.get('a')
        q = row.get('q')
        # Determine the input sampled at this row's posedge.
        if carried_a is None:
            sampled_a = a
        else:
            sampled_a = carried_a
        # If this row has a posedge (clk == 1), compute next settled state.
        if clk == 1:
            if state is None:
                # First settled value comes from the trace.
                state = q
            else:
                if sampled_a == 1:
                    pass  # hold
                else:
                    state = (state + 1) % 7
        # After sampling, a mid-cycle change may occur; carry it forward.
        # The printed `a` on this row is driven before the sampled edge,
        # so any change after sampling is represented by the next row's a.
        # We carry the current row's a forward as the post-sample value.
        carried_a = a
        results.append({'q': state if state is not None else 0})
    return results
