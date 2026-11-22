def reference(vectors):
    # State: COUNT holds current count value 0..9
    # Contract rules:
    #   R1_SYNC_RESET: reset==1 at posedge -> q=0 (priority 1)
    #   R2_COUNT_UP_WRAP: reset==0 at posedge -> q increments, wrapping 9->0 (priority 2)
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    # Power-up unspecified: start at 0.
    state = {"q": 0}
    out = []
    for row in vectors:
        # Sample: outputs driven before the sampled edge reflect current state
        # (values are driven before the sampled edge; we output current state)
        q = state["q"]
        out.append({"q": q & 0xF})
        # Apply posedge update using inputs at this row (reset)
        reset = row.get("reset", 0)
        if reset == 1:
            # R1_SYNC_RESET
            state["q"] = 0
        else:
            # R2_COUNT_UP_WRAP (candidate interpretation: saturate at 9)
            if state["q"] < 9:
                state["q"] = state["q"] + 1
            else:
                state["q"] = 9
        # Mid changes: applied after sampling, carried to next row.
        # (No mid inputs specified for this design beyond reset which is a
        #  normal input; nothing extra to do.)
    return out
