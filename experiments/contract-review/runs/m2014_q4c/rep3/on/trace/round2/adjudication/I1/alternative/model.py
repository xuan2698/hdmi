def reference(vectors):
    # Initial stored state: concrete 0 for unspecified power-up.
    q = 0
    out = []
    # global: candidate interpretation applied (negedge-triggered); state updates at each row's active edge.
    for row in vectors:
        r = row["r"]
        d = row["d"]
        # sync_active_high_reset: active-high synchronous reset forces q to 0 at the sampled edge.
        if r == 1:
            q = 0
        else:
            # d_capture_when_not_reset: capture d when reset is low at the sampled edge.
            q = d
        # Present q as a concrete unsigned 1-bit integer after the sampled edge has settled.
        q = 1 if q else 0
        out.append({"q": q})
    return out
