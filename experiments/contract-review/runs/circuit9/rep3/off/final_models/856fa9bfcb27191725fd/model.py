def reference(vectors):
    # Contract implementation.
    # State: q is a 3-bit counter. Initial value is 4 (no physical reset).
    # Rule hold_when_a_high: on posedge, if a==1, q holds.
    # Rule increment_when_a_low: on posedge, if a==0, q increments by 1 (mod 8).
    # Candidate interpretation for global: q initializes to 0; first posedge with a=1 sets q=4 (load),
    # then holds/increments per rules.
    # Mid input changes occur AFTER sampling, before the other edge, carried to start of next row.
    # Each row's values are driven before the sampled edge (posedge).

    q = 0  # global interpretation: initial q = 0
    loaded = False  # whether the initial load (a=1 -> q=4) has happened
    out = []

    for row in vectors:
        a = row.get('a', 0)
        # posedge sampling: apply transition based on current a
        if not loaded:
            # global interpretation: first posedge with a=1 sets q=4 (load)
            if a == 1:
                q = 4
                loaded = True
            # if a==0 before load, q stays 0 (no rule specified; keep 0)
        else:
            if a == 1:
                # hold_when_a_high
                pass
            else:
                # increment_when_a_low
                q = (q + 1) & 0x7
        out.append({'q': q & 0x7})

    return out
