def reference(vectors):
    # State: q (3-bit counter), initialized to None (x) until first posedge.
    # Rule hold_when_a_high: on posedge, if a==1, q holds.
    # Rule increment_when_a_low: on posedge, if a==0, q increments by 1 (mod 8),
    #   except the first posedge initializes q to 4 (from x).
    # First posedge: q becomes 4 regardless of a (per waveform: at 5ns a=1 -> q=4).
    # Subsequent posedges: a==1 -> hold; a==0 -> q = (q+1) % 8.
    q = None
    prev_a = None
    out = []
    for row in vectors:
        a = row['a']
        # posedge sampling
        if q is None:
            # first posedge initializes to 4
            q = 4
        else:
            if a == 1:
                # hold_when_a_high
                pass
            else:
                # increment_when_a_low
                q = (q + 1) % 8
        prev_a = a
        out.append({'q': q})
    return out
