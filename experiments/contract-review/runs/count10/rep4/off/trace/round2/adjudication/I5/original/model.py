def reference(vectors):
    # Contract implementation for a synchronous active-high-reset decade counter.
    # State: COUNT (0..9), updated on posedge clk.
    # R1: reset == 1 -> q = 0 on posedge (priority 1).
    # R2: reset == 0 && q < 9 -> q = q + 1 on posedge (priority 2).
    # R3: reset == 0 && q == 9 -> q = 0 on posedge (priority 2).
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.

    q = 0  # COUNT state, power-up unspecified but we start at 0
    out = []

    for row in vectors:
        reset = row.get("reset", 0)

        # Sample at posedge: compute next state based on current state and inputs.
        # R1: active high synchronous reset
        if reset == 1:
            q_next = 0
        # R2: count up while below 9
        elif q < 9:
            q_next = q + 1
        # R3: wrap from 9 to 0
        else:
            q_next = 0

        # Output visible same cycle (after posedge settles)
        out.append({"q": q_next & 0xF})

        # Mid changes occur AFTER sampling, before the other edge,
        # carried to the start of the next row. Apply them now.
        if "mid" in row and row["mid"]:
            for k, v in row["mid"].items():
                if k == "reset":
                    reset = v
                # (no other inputs to update)

        # Advance state for next row
        q = q_next

    return out
