def reference(vectors):
    # Contract: sequential circuit, 3-bit counter q.
    # R1: on posedge, if a == 1, q holds (priority 1).
    # R2: on posedge, if a == 0, q increments by 1 mod 8 (priority 2).
    # Reset: none. Power-up unspecified; use 4 as concrete initial value
    # (matches observed waveform where q=4 at first sample).
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    # Each row: values driven before sampled posedge; sample after posedge settles.

    q = 4  # concrete power-up value (unspecified by contract, chosen to match spec)
    out = []
    for row in vectors:
        a = row["a"]
        # R1: a == 1 -> hold on posedge
        if a == 1:
            q = q  # hold
        else:
            # R2: a == 0 -> increment on posedge
            q = (q + 1) & 0x7
        out.append({"q": q})
    return out
