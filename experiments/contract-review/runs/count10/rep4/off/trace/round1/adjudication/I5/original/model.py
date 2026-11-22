def reference(vectors):
    # State: COUNT holds current decade count 0..9
    # Contract rules:
    # R1: reset == 1 at posedge -> q = 0 (priority 1)
    # R2: reset == 0 && q < 9 at posedge -> q = q + 1
    # R3: reset == 0 && q == 9 at posedge -> q = 0
    # Power-up unspecified: start at 0 for concreteness.
    count = 0
    out = []
    for row in vectors:
        reset = row.get("reset", 0)
        # Sample at posedge: apply transition based on current state and inputs
        if reset == 1:
            # R1
            count = 0
        else:
            if count < 9:
                # R2
                count = count + 1
            else:
                # R3
                count = 0
        out.append({"q": count & 0xF})
    return out
