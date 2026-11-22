def reference(vectors):
    # Contract implementation for a synchronous active-high reset decade counter.
    # State: COUNT (0..9). Output q reflects the current count value.
    # R1_SYNC_RESET: reset == 1 at posedge -> q becomes 0 (same cycle visible).
    # R2_COUNT_INC: reset == 0 and q != 9 at posedge -> q increments.
    # R3_WRAP: reset == 0 and q == 9 at posedge -> q wraps to 0.
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.

    q = 0  # power-up unspecified; start at 0 for concrete outputs
    out = []

    for row in vectors:
        reset = row.get("reset", 0)

        # Sample at posedge: compute next state based on current inputs and state.
        # R1_SYNC_RESET (priority 0)
        if reset == 1:
            q_next = 0
        # R2_COUNT_INC (priority 1)
        elif q != 9:
            q_next = q + 1
        # R3_WRAP (priority 1)
        else:
            q_next = 0

        q = q_next
        out.append({"q": q & 0xF})

    return out
