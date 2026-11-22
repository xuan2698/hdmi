def reference(vectors):
    # Contract implementation for a simple D flip-flop with active-high synchronous reset.
    # State: Q (stored flip-flop value, driven to q). Updates on posedge clk.
    # R1: r == 1 on posedge -> q = 0 (synchronous reset, priority 1).
    # R2: r == 0 on posedge -> q = d (priority 2).
    # Power-up unspecified: initialize Q to 0 for concrete output.
    Q = 0  # named state
    out = []
    for row in vectors:
        d = int(row.get('d', 0)) & 1
        r = int(row.get('r', 0)) & 1
        # posedge sampling: apply rules
        if r == 1:
            # R1: active high synchronous reset
            Q = 0
        else:
            # R2: D flip-flop capture
            Q = d
        # drive output q from state Q
        out.append({'q': Q & 1})
    return out
