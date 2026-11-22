def reference(vectors):
    # R_RESET: synchronous active high reset clears out to 0
    # Candidate interpretation: reset clears the whole edge detector, so prev_in is cleared to 0
    out = 0
    prev_in = 0
    inputs = {"reset": 0, "in": 0}
    results = []
    MASK = 0xFFFFFFFF
    for row in vectors:
        # Apply row's explicit input values before the sampled posedge
        for key in row:
            if key != "mid":
                inputs[key] = row[key]
        # Sample inputs at posedge
        rst = inputs.get("reset", 0)
        inval = inputs.get("in", 0) & MASK
        if rst == 1:
            # R_RESET: reset has priority, clears out
            out = 0
            # Candidate interpretation: reset clears the whole edge detector
            prev_in = 0
        else:
            # R_FALL: detect 1-to-0 transitions and set out bits
            fall = prev_in & (~inval & MASK)
            # R_HOLD: out holds prior value; new falls set to 1
            out = (out | fall) & MASK
            # Update previous sampled input for next cycle
            prev_in = inval
        # Output visible same cycle after posedge
        results.append({"out": out})
        # Process mid input changes after sampling, before next row
        if "mid" in row:
            mid = row["mid"]
            for key in mid:
                inputs[key] = mid[key]
    return results
