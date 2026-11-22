def reference(vectors):
    # Contract implementation.
    # State: 3-bit counter q.
    # Rule hold_when_a_high (priority 1): on posedge, if a==1, q holds.
    # Rule increment_when_a_low (priority 2): on posedge, if a==0, q increments (mod 8).
    # Reset: none. Initial q unspecified; use 4 as the observed power-up value
    # (matches waveform: first posedge with a=1 yields q=4).
    # Mid: none.
    q = 4  # initial counter value (unspecified at power-up; 4 per waveform)
    out = []
    for row in vectors:
        a = row["a"]
        # posedge update
        if a == 1:
            # hold_when_a_high
            pass
        else:
            # increment_when_a_low
            q = (q + 1) & 0x7
        out.append({"q": q})
    return out
