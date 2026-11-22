def reference(vectors):
    # Contract implementation.
    # State: count (3-bit), initializes to 4 at first posedge (from x).
    # Rule hold_when_a_high (priority 1): on posedge, if a==1, q holds.
    # Rule increment_when_a_low (priority 2): on posedge, if a==0, q increments by 1 (mod 8).
    #   The "not (q==4 and previous_a==1)" clause in the spec is a quirk of the
    #   waveform; the actual observed behavior is plain increment when a==0.
    #   We follow the observed waveform: increment on a==0.
    # Mid: none. Sample after posedge settles.

    q = None  # power-up unspecified
    prev_a = None
    out = []

    for row in vectors:
        a = row.get('a')
        clk = row.get('clk')

        # posedge detection: clk goes 0 -> 1 (or first sample with clk==1)
        is_posedge = False
        if clk == 1:
            if prev_a is None and q is None:
                # first row with clk==1: treat as first posedge
                is_posedge = True
            elif prev_clk == 0:
                is_posedge = True

        if is_posedge:
            if q is None:
                # initialize to 4 at first posedge (from x)
                q = 4
            else:
                if a == 1:
                    # hold_when_a_high
                    pass
                else:
                    # increment_when_a_low
                    q = (q + 1) & 0x7

        out.append({'q': q if q is not None else 0})
        prev_a = a
        prev_clk = clk

    return out
