def reference(vectors):
    # 3-bit up-counter with hold control.
    # On each posedge: if a==1 hold q; else q <= (q+1) mod 8.
    # q is a registered output (updates one cycle after sampled posedge).
    # Initial q value is unspecified; use 4 as observed in trace.
    q = 4
    out = []
    for row in vectors:
        clk = row.get('clk', 0)
        a = row.get('a', 0)
        # Sample on posedge
        if clk == 1:
            if a == 1:
                pass  # hold
            else:
                q = (q + 1) % 8
        out.append({'q': q & 0x7})
    return out
